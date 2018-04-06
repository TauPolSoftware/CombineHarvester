# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys

import CombineHarvester.ZTTPOL2016.datacards as datacards

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.ZTTPOL2016.zttpol2016_datacards as zttdatacards
import CombineHarvester.ZTTPOL2016.zttpol2016_systematics as zttpol_systematics

#Colors
OKGREEN = '\033[92m'
WARNING = '\033[93m'
ENDC = '\033[0m'

def CreateDatacard(zttdatacards):
    '''Create an instance of the python datacards modul, which includes a combine harvester instance.'''
    try:
        datacards = zttdatacards.ZttPolarisationDatacards()

        
    except:
        print "CreateDatacard failed:"
        (ty, val, tb)=sys.exc_info()
        print WARNING + "Err Type : " + ENDC, ty
        print WARNING + "Err Value: " + ENDC, val
        print WARNING + "Trace    : " + ENDC, tb

    return datacards

def ExtractShapes():
    '''Extract the Shape uncertainties from root input histograms. '''

    return None

def ScaleSignalProcess():

    return None

def BinErrorsAndBBB():

    return None

def FilterSystematics():

    return None

def WriteDatacard():

    return None





if __name__ == "__main__":
    #Arguments for the ArgParse parser
    parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT polarisation analysis.",
                                     parents=[logger.loggingParser])

    parser.add_argument("-i", "--input-dir", required=False,
                        help="Input directory.")

    #Create Datacards
    print OKGREEN + '----- Creating datacard with processes and systematics...    -----' + ENDC
    datacards = CreateDatacard(zttdatacards)

    print OKGREEN + '----- Adding systematic uncertainties...                     -----' + ENDC

    print OKGREEN + '----- Extracting histograms from input root files...         -----' + ENDC

    print OKGREEN + '----- Scaling signal process rates...                        -----' + ENDC

    print OKGREEN + '----- Merging bin errors and generating bbb uncertainties... -----' + ENDC

    print OKGREEN + '----- Setting standardised bin names...                      -----' + ENDC

    print OKGREEN + '----- Done                                                   -----' + ENDC
