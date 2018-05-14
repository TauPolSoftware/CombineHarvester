
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

def CreateDatacard(args):
    '''Create an instance of the python datacards modul, which includes a combine harvester instance.'''

    datacards = zttdatacards.ZttPolarisationDatacards()

    for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):

        # prepare category settings based on args and datacards
        if (len(categories) == 1) and (categories[0] == "all"):
            categories = datacards.cb.cp().channel([channel]).bin_set()
        else:
            categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
        args.categories[index] = categories

        # restrict CombineHarvester to configured categories:
        datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))

        datacards.cb.channel(args.channel)

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

    #datacards.cb.SetGroup("bbb", [".*_bin_\\d+"])

    return None

def WriteDatacard(datacards, datacard_filename_template, root_filename_template, output_directory):
    ''' Write datacards. '''
    
    # http://cms-analysis.github.io/CombineHarvester/classch_1_1_card_writer.html#details
    writer = ch.CardWriter(os.path.join("$TAG", datacard_filename_template),
                           os.path.join("$TAG", root_filename_template))

    # enable writing datacards in cases where the mass does not have its original meaning
    if (len(datacards.cb.mass_set()) == 1) and (datacards.cb.mass_set()[0] == "*"):
        writer.SetWildcardMasses([])

    return writer.WriteCards(output_directory[:-1] if output_directory.endswith("/") else output_directory, datacards.cb)

def text2workspace(datacards, datacards_cbs, Physicsmodel, workspace_file_name):

    commands = ["text2workspace.py -m {MASS} -P {PHYSICSMODEL} {DATACARD} -o {OUTPUT}".format(
            PHYSICSMODEL=Physicsmodel,
            MASS= 0, #datacards.cb.mass_set()[0],
            DATACARD=datacard,
            OUTPUT=os.path.splitext(datacard)[0]+"_"+workspace_file_name+".root"
    ) for datacard, cb in datacards_cbs.iteritems()]

    #tools.parallelize(_call_command, commands, n_processes=4, description="text2workspace.py")
    for command in commands:
        os.system(command)

    return {datacard : os.path.splitext(datacard)[0]+"_workspace"+".root" for datacard in datacards_cbs.keys()}

def use_asimov_dataset(datacards, pol=-0.159, r=1.0, signal_mass = None, signal_processes=None):

    def _replace_observation_by_asimov_dataset(observation):
        cb = datacards.cb.cp().analysis([observation.analysis()]).era([observation.era()]).channel([observation.channel()]).bin([observation.bin()])
        background = cb.cp().backgrounds()

        signal = cb.cp().signals()
        if signal_mass:
            if signal_processes:
                signal = cb.cp().signals().process(signal_processes).mass([signal_mass])
            else:
                signal = cb.cp().signals().mass([signal_mass])
        elif signal_processes:
            signal = cb.cp().signals().process(signal_processes)

        observation.set_shape(background.GetShape() + signal.GetShape(), True)
        observation.set_rate(background.GetRate() + signal.GetRate())

    pospol_signals = datacards.cb.cp().signals()
    pospol_signals.FilterAll(lambda obj : ("pospol" not in obj.process().lower()))

    negpol_signals = datacards.cb.cp().signals()
    negpol_signals.FilterAll(lambda obj : ("negpol" not in obj.process().lower()))

    pospol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (r * (1.0 + pol) / 2.0)))
    negpol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (r * (1.0 - pol) / 2.0)))
    
    datacards.cb.cp().ForEachObs(_replace_observation_by_asimov_dataset)
    
    pospol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() / (r * (1.0 + pol) / 2.0)))
    negpol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() / (r * (1.0 - pol) / 2.0)))


    return datacards


def MultiDimFit_TotStatUnc(datacards, datacards_workspaces, datacards_cbs, args,algo = "singles"):
    
    stable_options = r"--robustFit 1 --preFitValue 1.0 --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo Minuit2 --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:1.0"

    method = "MultiDimFit"
    tmp_args = "-M MultiDimFit --algo " + algo + " -P pol --redefineSignalPOIs pol "+stable_options+" -n "
    name = re.search("(-n|--name)[\s=\"\']*(?P<name>\w*)[\"\']?\s", tmp_args)
    name = name.groupdict()["name"]
    datacards_poi_ranges = {}

    chunks = [[chunk*199, (chunk+1)*199-1] for chunk in xrange(200/199+1)]

    split_stat_syst_uncs_options = [
        "--saveWorkspace",
        "--snapshotName {method} -w w".format(method=method),
        "--snapshotName {method} -w w --freezeNuisanceGroups syst".format(method=method, uncs="{uncs}"), #.format(uncs=datacards_cbs[datacard].syst_name_set())
    ]
    split_stat_syst_uncs_names = [
        "Workspace",
        "TotUnc",
        "StatUnc",
    ]

    for split_stat_syst_uncs_index, (split_stat_syst_uncs_option, split_stat_syst_uncs_name) in enumerate(zip(split_stat_syst_uncs_options, split_stat_syst_uncs_names)):
        prepared_tmp_args = None

        new_name = ("" if name is None else name) + " " + split_stat_syst_uncs_name
        if name is None:
            prepared_tmp_args = tmp_args +new_name
        else:
            prepared_tmp_args = copy.deepcopy(tmp_args)
            prepared_tmp_args = re.sub("(--algo)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2 "+("none" if split_stat_syst_uncs_index == 0 else "\\3")+"\\4", prepared_tmp_args)
            prepared_tmp_args = re.sub("(-n|--name)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2"+new_name+"\\4", prepared_tmp_args)

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

        tools.parallelize(_call_command, commands, n_processes=4, description="combine")
    
    return datacards
