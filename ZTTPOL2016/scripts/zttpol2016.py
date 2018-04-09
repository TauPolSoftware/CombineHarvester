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
FAIL = '\033[91m'
ENDC = '\033[0m'

def CreateDatacard(zttdatacards):
    '''Create an instance of the python datacards modul, which includes a combine harvester instance.'''
    try:
        datacards = zttdatacards.ZttPolarisationDatacards()

        #Modify the datacard
        datacards.cb

    except:
        print FAIL + "Extracting Shapes from input files failed:" + ENDC
        (ty, val, tb)=sys.exc_info()
        print FAIL + "Error on line :" + ENDC + '{}'.format(sys.exc_info()[-1].tb_lineno)
        print FAIL + "Err Type      :" + ENDC, ty
        print FAIL + "Err Value     :" + ENDC, val
        print FAIL + "Trace         :" + ENDC, tb

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

def hp_inputsfromsamples():

    return None


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
if __name__ == "__main__":
    #Arguments for the ArgParse parser
    parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT polarisation analysis.",
                                     parents=[logger.loggingParser])

    parser.add_argument("-i", "--input-dir", required=False,
                        help="Input directory of the root files. In case of HP for the samples.")
    parser.add_argument("-c", "--channel", action = "append",
                        default=["mt", "et", "tt", "em"],
                       help="Channel. This agument can be set multiple times. [Default: %(default)s]")
    parser.add_argument("--categories", action="append", nargs="+",
                        default=[["all"]] * len(parser.get_default("channel")),
                       help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
    parser.add_argument("--HarryPlotter", default = False,
                        help = "Use HarryPlotter for extracting shapes")

    args = parser.parse_args()

    #1.Create Datacards
    print OKGREEN + '----- Creating datacard with processes and systematics...    -----' + ENDC

    datacards = CreateDatacard(zttdatacards)

    datacards.cb.channel(args.channel)

    for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):

        # prepare category settings based on args and datacards
        if (len(categories) == 1) and (categories[0] == "all"):
            categories = datacards.cb.cp().channel([channel]).bin_set()
        else:
            categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
        args.categories[index] = categories

        # restrict CombineHarvester to configured categories:
        datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))

    #DEBUG
    print WARNING + "datacards: channel_set" + ENDC, datacards.cb.channel_set()
    print WARNING + "datacards: bin_set" + ENDC, datacards.cb.bin_set()

    #2.Extract shapes from input root files or from samples with HP
    print OKGREEN + '----- Extracting histograms from input root files...         -----' + ENDC

    if not args.HarryPlotter:
        try:
            for chn in datacards.cb.channel_set():
                file = args.input_dir + "ztt_" + chn + ".root"
                datacards.cb.cp().channel([chn]).backgrounds().ExtractShapes(
                    file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC'
                )
                datacards.cb.cp().channel([chn]).backgrounds().ExtractShapes(
                    file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC'
                )
        except Exception as e:
            print FAIL + "Extracting Shapes from input files failed:" + ENDC
            (ty, val, tb)=sys.exc_info()
            print FAIL + "Error on line :" + ENDC + '{}'.format(sys.exc_info()[-1].tb_lineno)
            print FAIL + "Err Type      :" + ENDC, ty
            print FAIL + "Err Value     :" + ENDC, val
            print FAIL + "Trace         :" + ENDC, tb
    else:
        hp_inputsfromsamples()


    print OKGREEN + '----- Scaling signal process rates...                        -----' + ENDC

    print OKGREEN + '----- Merging bin errors and generating bbb uncertainties... -----' + ENDC

    print OKGREEN + '----- Setting standardised bin names...                      -----' + ENDC

    print OKGREEN + '----- Done                                                   -----' + ENDC
