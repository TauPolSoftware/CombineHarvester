#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import argparse
import copy
import os
import sys
import re
import glob

import ROOT

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.ZTTPOL2016.zttpol2016_datacards as zttdatacards

import CombineHarvester.ZTTPOL2016.tools as tools
from CombineHarvester.ZTTPOL2016.tools import _call_command

#Colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def CreateDatacard():
    '''Create an instance of the python datacards modul, which includes a combine harvester instance.'''

    datacards = zttdatacards.ZttPolarisationDatacards()

    return datacards


def ExtractShapes(datacards,input_dir):
    '''Extract the Shape uncertainties from root input histograms. '''
    #Find the files present in the input_dir
    files_in_input_dir = [file.split("_") for file in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, file))]
    categories_in_input_dir = [reduce( lambda x,y: x + "_" + y, strings[2:-1]) for strings in files_in_input_dir]

    for chn in datacards.cb.channel_set():
        bins = filter(lambda bin: bin.split('_')[0] == chn,datacards.cb.bin_set())
        bins = filter(lambda x: categories_in_input_dir.count(x) >= 1, bins)
        for bin in bins:
            try:
                #Background shapes
                file = input_dir + "/ztt_" + chn +"_" + bin + "_13TeV.root"
                datacards.cb.cp().channel([chn]).bin([bin]).backgrounds().ExtractShapes(
                   file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC'
                )
                #Signal shapes
                datacards.cb.cp().channel([chn]).bin([bin]).signals().ExtractShapes(
                    file, '$BIN/$PROCESS', '$BIN/$PROCESS'
                )
                print OKGREEN + 'Extracting Shapes for:' + ENDC, bin
            except Exception as e:
                print FAIL + "Extracting Shapes from input files failed:" + ENDC
                (ty, val, tb)=sys.exc_info()
                print FAIL + "Error on line :" + ENDC + '{}'.format(sys.exc_info()[-1].tb_lineno)
                print FAIL + "Err Type      :" + ENDC, ty
                print FAIL + "Err Value     :" + ENDC, val
                print FAIL + "Trace         :" + ENDC, tb

    return datacards


def BinErrorsAndBBB(datacards, AddThreshold, MergeTreshold, FixNorm):
    '''Function to add bin by bin uncertainties. '''

    bbb = ch.BinByBinFactory()
    bbb.SetAddThreshold(AddThreshold).SetMergeThreshold(MergeTreshold).SetFixNorm(FixNorm)
    bbb.MergeBinErrors(datacards.cb.cp().backgrounds())
    bbb.AddBinByBin(datacards.cb.cp().backgrounds(), datacards.cb)

    datacards.cb.SetGroup("bbb", [".*_bin_\\d+"])

    return None


def WriteDatacard(datacards,output_dir):
    ''' Write datacards. '''

    writer = ch.CardWriter(os.path.join(output_dir + "/zttpol_datacard.txt"),
                           os.path.join(output_dir + "/zttpol_datacard_rootfile.root"))

    return writer.WriteCards(output_dir, datacards.cb)
