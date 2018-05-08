#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import argparse
import copy
import os
import sys
import re
import glob
from types import *

import ROOT

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.ZTTPOL2016.zttpol2016_datacards as zttdatacards

import CombineHarvester.ZTTPOL2016.tools as tools
from CombineHarvester.ZTTPOL2016.tools import _call_command

from CombineHarvester.ZTTPOL2016.zttpol2016_functions import *

#Colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
if __name__ == "__main__":
    #Arguments for the ArgParse parser
    parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT polarisation analysis.")

    parser.add_argument("-i", "--input-dir", required=False,
                        help="Input directory of the root files. In case of HP for the samples.")
    parser.add_argument("-c", "--channel", action = "append",
                        default=["mt", "et", "tt", "em"],
                       help="Channel. This agument can be set multiple times. [Default: %(default)s]")
    parser.add_argument("--categories", action="append", nargs="+",
                        default=[["all"]] * len(parser.get_default("channel")),
                       help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
    parser.add_argument("-o", "--output-dir",
                        help="Output directory. [Default: %(default)s]")
    parser.add_argument("--SMHTTsystematics", action="store_true", default = False,
                        help = "Use the SM HTT2016 Systematics.")
    parser.add_argument("-a", "--analysis", action = "store_true", default = False,
                        help = "Perform an Statistical Analysis")
    parser.add_argument("--no-shape-uncs", default=False, action="store_true",
                        help="Do not include shape-uncertainties. [Default: %(default)s]")
    parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
                        help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")

    args = parser.parse_args()

    if args.channel != parser.get_default("channel"):
        args.channel = args.channel[len(parser.get_default("channel")):]

    if args.categories != parser.get_default("categories"):
        args.categories = args.categories[len(parser.get_default("categories")):]
    args.categories = (args.categories * len(args.channel))[:len(args.channel)]


    #1.-----Create Datacards
    print WARNING + UNDERLINE + '-----      Creating datacard with processes and systematics...        -----' + ENDC

    datacards = CreateDatacard(args)
    if args.SMHTTsystematics:
        datacards.AddHTTSM2016Systematics()


    if args.no_shape_uncs:
        print("No shape uncs")
        datacards.cb.FilterSysts(lambda systematic : systematic.type() == "shape")

    print OKGREEN + 'Datacard channels:' + ENDC, datacards.cb.channel_set()
    print OKGREEN + 'Datacard categories :' + ENDC, datacards.cb.bin_set()
    print OKGREEN + 'Datacard systematics :' + ENDC, datacards.cb.syst_name_set()


    #2.-----Extract shapes from input root files or from samples with HP
    print WARNING + '-----      Extracting histograms from input root files...             -----' + ENDC
    assert type(args.input_dir) is not NoneType, FAIL + "Input dir is not specified" + ENDC
    assert type(args.output_dir) is not NoneType, FAIL + "Output dir is not specified" + ENDC

    ExtractShapes(datacards, args.input_dir)
    datacards.cb.SetGroup("syst", [".*"])

    #3.-----Add BBB
    print WARNING + '-----      Merging bin errors and generating bbb uncertainties...     -----' + ENDC

    BinErrorsAndBBB(datacards, 0.1, 0.5, True)
    datacards.cb.SetGroup("syst_plus_bbb", [".*"])

    #4.-----Write Cards
    print WARNING + '-----      Writing Datacards...                                       -----' + ENDC

    datacards_cbs = WriteDatacard(datacards, args.output_dir)

    #5.-----Done
    print WARNING + '-----      '+OKGREEN+'Done'+WARNING +'                                                       -----' + ENDC

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ StatisticalAnalysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
    if args.analysis:
        print WARNING + UNDERLINE  + '-----      Performing statistical analysis                            -----' + ENDC

        if args.use_asimov_dataset:
            datacards = use_asimov_dataset(datacards)
            print OKGREEN + "Using asimov dataset!" + ENDC

        #6.-----text2workspace
        print WARNING + '-----      text2workspace                                             -----' + ENDC

        physicsmodel = "CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol"
        datacards_workspaces = text2workspace(datacards,datacards_cbs,physicsmodel,"workspace")

        #7.-----totstatuncs
        print WARNING + '-----      Tot and stat uncs                                          -----' + ENDC

        MultiDimFit_TotStatUnc(datacards, datacards_workspaces, datacards_cbs, args,algo = "singles")