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

    datacards = CreateDatacard()
    if args.SMHTTsystematics:
        datacards.AddHTTSM2016Systematics()

    datacards.cb.channel(args.channel)

    if args.no_shape_uncs:
        print("No shape uncs")
        datacards.cb.FilterSysts(lambda systematic : systematic.type() == "shape")


    for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):

        # prepare category settings based on args and datacards
        if (len(categories) == 1) and (categories[0] == "all"):
            categories = datacards.cb.cp().channel([channel]).bin_set()
        else:
            categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
        args.categories[index] = categories

        # restrict CombineHarvester to configured categories:
        datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))

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
        print OKBLUE + "datacards observations: " + ENDC, datacards.cb.PrintProcs()

        #6.-----text2workspace
        print WARNING + '-----      text2workspace                                             -----' + ENDC

        physicsmodel = "CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol"
        datacards_workspaces = text2workspace(datacards,datacards_cbs,physicsmodel,"workspace")

        #7.-----totstatuncs
        print WARNING + '-----      Tot and stat uncs                                          -----' + ENDC

        stable_options = r"--robustFit 1 --preFitValue 1.0 --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo Minuit2 --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:1.0"

        method = "MultiDimFit"
        tmp_args = "-M MultiDimFit --algo singles -P pol --redefineSignalPOIs pol "+stable_options+" -n "
        name = re.search("(-n|--name)[\s=\"\']*(?P<name>\w*)[\"\']?\s", tmp_args)
        name = name.groupdict()["name"]
        datacards_poi_ranges = {}

        chunks = [[chunk*199, (chunk+1)*199-1] for chunk in xrange(200/199+1)]

        split_stat_syst_uncs_options = [
            "--saveWorkspace",
            "--snapshotName {method} -w w".format(method=method),
            "--snapshotName {method} -w w --freezeNuisanceGroups syst_plus_bbb".format(method=method, uncs="{uncs}"), #.format(uncs=datacards_cbs[datacard].syst_name_set())
        ]
        split_stat_syst_uncs_names = [
            "Workspace",
            "TotUnc",
            "StatUnc",
        ]

        for split_stat_syst_uncs_index, (split_stat_syst_uncs_option, split_stat_syst_uncs_name) in enumerate(zip(split_stat_syst_uncs_options, split_stat_syst_uncs_names)):
            prepared_tmp_args = None

            new_name = ("" if name is None else name) + split_stat_syst_uncs_name
            if name is None:
                prepared_tmp_args = tmp_args + " -n " + new_name
            else:
                prepared_tmp_args = copy.deepcopy(tmp_args)
                prepared_tmp_args = re.sub("(--algo)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2 "+("none" if split_stat_syst_uncs_index == 0 else "\\3")+"\\4", prepared_tmp_args)
                prepared_tmp_args = re.sub("(-n|--name)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2"+new_name+"\\4", prepared_tmp_args)

            prepared_tmp_args = re.sub("-n -n", "-n ", prepared_tmp_args)

            commands = []
            for chunk_index, (chunk_min, chunk_max) in enumerate(chunks):
                commands.extend([[
                        "combine -m {MASS} {POI_RANGE} {ARGS} {CHUNK_POINTS} {SPLIT_STAT_SYST_UNCS} {WORKSPACE}".format(
                                MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else 91,
                                POI_RANGE="--rMin {RMIN} --rMax {RMAX}" if datacard in datacards_poi_ranges else "",
                                ARGS=prepared_tmp_args.format(CHUNK=str(chunk_index), RMIN="{RMIN}", RMAX="{RMAX}"),
                                CHUNK_POINTS = "" if (chunk_min is None) or (chunk_max is None) else "--firstPoint {CHUNK_MIN} --lastPoint {CHUNK_MAX}".format(
                                        CHUNK_MIN=chunk_min,
                                        CHUNK_MAX=chunk_max
                                ),
                                SPLIT_STAT_SYST_UNCS=split_stat_syst_uncs_option,
                                WORKSPACE="-d " + workspace
                        ).format(RMIN=datacards_poi_ranges.get(datacard, ["", ""])[0], RMAX=datacards_poi_ranges.get(datacard, ["", ""])[1]),
                        os.path.dirname(workspace)
                ] for datacard, workspace in datacards_workspaces.iteritems()])

            #tools.parallelize(_call_command, commands, n_processes=4, description="combine")
            for command in commands:
                print OKGREEN + "combine call: " + ENDC, command[0] , "\n"
                os.system(command[0])


            #for datacard, workspace in datacards_workspaces.items():
            #    datacards_workspaces[datacard] = glob.glob(os.path.join(os.path.dirname(workspace), "higgsCombine"+new_name+"."+method+".*.root"))

            break
