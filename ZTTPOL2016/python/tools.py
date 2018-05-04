# -*- coding: utf-8 -*-

import logging

import array
import copy
import fcntl
import multiprocessing
import os
import re
import sys
import termios
import textwrap
import shlex
import subprocess
import time
import ROOT
import math



class ProgressIterator(object):

	def __init__(self, iterable, length=None, description="", visible=True):
		self.iterator = iter(iterable)
		self.len = length if length != None else len(iterable)
		self.description = (description if description == "" else (description+"... "))
		self.current_index = 0
		self.ratio = -1.0
		self.tty_width = get_tty_size()[1]
		self.visible = visible

	def __iter__(self):
		return self

	def next(self):
		ratio = float(self.current_index) / self.len

		if int(ratio*100) > int(self.ratio*100):
			self.ratio = ratio
			current_progress = min(int(math.ceil(float(self.tty_width) * self.current_index / self.len)),
		                       self.tty_width)

			line = "%s%.1f %s" % (self.description, ratio*100, "%")
			#line += (" " * (self.tty_width - len(line)))
			line = line.center(self.tty_width)
			line = "\r\033[0;42m%s\033[0;41m%s\033[0m" % (line[:current_progress], line[current_progress:])
			if self.visible:
				sys.stdout.write(line)
				sys.stdout.flush()

		if (self.current_index == self.len-1) and self.visible:
			sys.stdout.write("\r\033[J")
			sys.stdout.flush()

		self.current_index += 1
		try:
			return self.iterator.next()
		except StopIteration, e:
			sys.stdout.write("\r\033[J")
			sys.stdout.flush()
			raise StopIteration(e)




def get_tty_size():
	size = array.array("B", [0, 0, 0, 0])
	try:
		fcntl.ioctl(0, termios.TIOCGWINSZ, size, True)
		return (size[0], size[2])
	except:
		return size

def parallelize(function, arguments_list, n_processes=1, description=None):
	if n_processes <= 1:
		results = []
		for arguments in arguments_list:
			results.append(function(arguments))
		return results
	else:
		pool = multiprocessing.Pool(processes=max(1, min(n_processes, len(arguments_list))))
		results = pool.map_async(function, arguments_list, chunksize=1)
		n_tasks = len(arguments_list)
		left = n_tasks-1
		progress_iterator = ProgressIterator(range(n_tasks), description=(description if description else "calling "+str(function)))
		progress_iterator.next()
		while (True):
			ready = results.ready()
			remaining = results._number_left
			if ready or (remaining < left):
				for i in range(left-remaining):
					progress_iterator.next()
				left = remaining
			if ready:
				break
			time.sleep(1.0)
		returnvalue = results.get(9999999)
		pool.close() # necessary to actually terminate the processes
		pool.join()  # without these two lines, they happen to live until the whole program terminates
		return returnvalue

def _call_command(args):
	command = None
	cwd = None
	if isinstance(args, basestring):
		command = args
	else:
		command = args[0]
		if len(args) > 1:
			cwd = args[1]

	old_cwd = None
	if not cwd is None:
		old_cwd = os.getcwd()
		os.chdir(cwd)
	print '\033[94m' + "Executing command: " + '\033[0m',command
	#log.debug(command)
	#logger.subprocessCall(command, shell=True)
	os.system(command)
	
	if not cwd is None:
		os.chdir(old_cwd)
