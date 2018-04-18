# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

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
                file = args.input_dir + "/ztt_" + chn +"_" + bin + "_13TeV.root"
                datacards.cb.cp().channel([chn]).bin([bin]).backgrounds().ExtractShapes(
                   file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC'
                )
                datacards.cb.cp().channel([chn]).bin([bin]).backgrounds().ExtractShapes(
                    file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC'
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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
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
    parser.add_argument("-o", "--output-dir",
                        default="$CMSSW_BASE/src/plots/ztt_polarisation_datacards/",
                        help="Output directory. [Default: %(default)s]")
    parser.add_argument("--SMHTTsystematics", action="store_true", default = False,
                        help = "Use the SM HTT2016 Systematics.")
    parser.add_argument("-a", "--analysis", action = "store_true", default = False,
                        help = "Perform an Statistical Analysis")
    parser.add_argument("--no-shape-uncs", default=False, action="store_true",
	                    help="Do not include shape-uncertainties. [Default: %(default)s]")
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

    ExtractShapes(datacards, args.input_dir)
    #datacards.cb.SetGroup("syst", [".*"])

    #3.-----Add BBB
    print WARNING + '-----      Merging bin errors and generating bbb uncertainties...     -----' + ENDC

    BinErrorsAndBBB(datacards, 0.1, 0.5, True)
    #datacards.cb.SetGroup("syst_plus_bbb", [".*"])

    #4.-----Write Cards
    print WARNING + '-----      Writing Datacards...                                       -----' + ENDC

    datacards_cbs = WriteDatacard(datacards, args.output_dir)

    #5.-----Done
    print WARNING + '-----      Done                                                       -----' + ENDC

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ StatisticalAnalysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
    if args.analysis:
        print WARNING + UNDERLINE  + '-----      Performing statistical analysis                            -----' + ENDC

        #6.-----text2workspace
        print WARNING + '-----      text2workspace                                             -----' + ENDC

        physicsmodel = "TauPolSoftware.StatisticalAnalysis.taupolarisationmodels:ztt_pol"

        commands = ["text2workspace.py -m {MASS} -P {PHYSICSMODEL} {DATACARD} -o {OUTPUT}".format(
                PHYSICSMODEL=physicsmodel,
                MASS= 0, #datacards.cb.mass_set()[0],
                DATACARD=datacard,
                OUTPUT=os.path.splitext(datacard)[0]+"_workspace"+".root"
        ) for datacard, cb in datacards_cbs.iteritems()]

        #tools.parallelize(_call_command, commands, n_processes=4, description="text2workspace.py")
        for command in commands:
            os.system(command)

        datacards_workspaces = {datacard : os.path.splitext(datacard)[0]+"_workspace"+".root" for datacard in datacards_cbs.keys()}


        """
        #7.-----totstatuncs
        print WARNING + '-----      Tot and stat uncs                                          -----' + ENDC

        split_stat_syst_uncs_options = [""]
        split_stat_syst_uncs_names = [""]

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
                ] for datacard, workspace in datacards_workspaces.items()])

            #tools.parallelize(_call_command, commands, n_processes=4, description="combine")
            for command in commands:
                os.system(command[0]+command[1])

            for datacard, workspace in datacards_workspaces.items():
                print OKBLUE + "glob.glob :" + ENDC, (os.path.join(os.path.dirname(workspace), "higgsCombine"+new_name+"."+method+".*.root"))


            #for datacard, workspace in datacards_workspaces.items():
            #    datacards_workspaces[datacard] = glob.glob(os.path.join(os.path.dirname(workspace), "higgsCombine"+new_name+"."+method+".*.root"))
        """
