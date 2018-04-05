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
import CombineHarvester.ZTTPOL2016.zttpol2016_systematics as zttpol_systematics


if __name__ == "__main__":

    chns = ['et', 'mt', 'em', 'tt']

    input_folders = {
      'et' : 'et',
      'mt' : 'mt',
      'em' : 'em',
      'tt' : 'tt'
    }

    datacards = ZttPolarisationDatacards() # Initiate combine harvester instance and add processes and systematics

    datacards.cb.channel(["mt","et","tt","em"])

    #Extracting shapes

    for chn in chns:
        file = input_folders[chn] + ".root"
        datacards.channel([chn]).era([era]).backgrounds().ExtractShapes(
            file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
        datacards.channel([chn]).era([era]).signals().ExtractShapes(
            file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')

    #Bin errors and bin-by-bin uncertainties

    bbb = datacards.BinByBinFactory()
