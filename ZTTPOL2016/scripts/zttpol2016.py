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

def CreateDatacard(zttdatacards):

    datacards = zttdatacards.ZttPolarisationDatacards()

    return datacards

def ExtractShapes():

    return None

def ScaleSignalProcess():

    return None

def BinErrorsAndBBB():

    return None

def FilterSystematics():

    return None

def Write Datacard():

    return None





if __name__ == "__main__":

    cb = ch.CombineHarvester()



    #Extracting shapes

    #Bin errors and bin-by-bin uncertainties

    print '----- Creating processes and observations...                 -----'
    datacards = CreateDatacard(zttdatacards)

    print '----- Adding systematic uncertainties...                     -----'

    print '----- Extracting histograms from input root files...         -----'

    print '----- Scaling signal process rates...                        -----'

    print '----- Merging bin errors and generating bbb uncertainties... -----'

    print '----- Setting standardised bin names...                      -----'

    print '----- Done                                                   -----'
