# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import CombineHarvester.ZTTPOL2016.datacards as datacards

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.ZTTPOL2016.zttpol2016_systematics as Systematics


def AddSystematic(cb, name, channels, processes):
    ''' Add a systematic to a combine harvester instance. '''

    if not channels == None:
        for channel in channels.split(","):
            cb.cp().channel([channel]).process(processes.split(",")).AddSyst(cb, *Systematics.name)
    else:
        cb.cp().process(processes.split(",")).AddSyst(cb, *Systematics.name)
    return cb



class ZttPolarisationDatacards(datacards.Datacards):
    ''' Datacard class for the polarisation analysis. '''

    def __init__(self, cb=None):
        super(ZttPolarisationDatacards, self).__init__(cb)

        if cb is None:

            # ==================================================================
            # mt channel
            self.add_processes(
                    channel="mt",
                    categories=["mt_"+category for category in ["rho", "oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )

            # mt systematics
            AddSystematic(self.cb, muon_efficiency_syst_args, ["mt"], ["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"])

            AddSystematic(self.cb, tau_efficiency_corr_syst_args, ["mt"], ["ZTTPOSPOL", "ZTTNEGPOL"])
            AddSystematic(self.cb, tau_es_syst_args, ["mt"], ["ZTTPOSPOL", "ZTTNEGPOL"])

            # from Yuta
            AddSystematic(self.cb, boson_scale_met_syst_args, ["mt"], ["ZL", "ZJ", "W"])
            AddSystematic(self.cb, boson_resolution_met_syst_args, ["mt"], ["ZL", "ZJ", "W"])
            AddSystematic(self.cb, ewk_top_scale_met_syst_args, ["mt"], ["TT", "VV"])
            AddSystematic(self.cb, ewk_top_resolution_met_syst_args, ["mt"], ["TT", "VV"])

            # extrapolation uncertainty
            AddSystematic(self.cb, ttj_extrapol_syst_args, ["mt"], ["TT"])
            AddSystematic(self.cb, wj_extrapol_syst_args, ["mt"], ["W"])

            # Tau Es
            AddSystematic(self.cb, tau_es_syst_args, ["mt"], ["ZTTPOSPOL", "ZTTNEGPOL"])

            # fake-rate
            AddSystematic(self.cb, eFakeTau_vloose_syst_args, ["mt"], ["ZL"])
            AddSystematic(self.cb, muFakeTau_syst_args, ["mt"], ["ZL"])
            AddSystematic(self.cb, zjFakeTau_syst_args, ["mt"], ["ZJ"])

            # ==================================================================
            # et channel
            self.add_processes(
                    channel="et",
                    categories=["et_"+category for category in ["rho", "oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )

            # et systematics

            # ==================================================================
            # tt channel
            self.add_processes(
                    channel="tt",
                    categories=["tt_"+category for category in ["rho", "rho_1", "rho_2", "oneprong", "combined_oneprong_oneprong", "combined_rho_rho"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )

            # tt systematics

            # ==================================================================
            # em channel
            self.add_processes(
                    channel="em",
                    categories=["em_"+category for category in ["oneprong"]],
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )
