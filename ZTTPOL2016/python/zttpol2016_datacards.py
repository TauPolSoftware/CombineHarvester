# -*- coding: utf-8 -*-

import logging
import copy
import re

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.ZTTPOL2016.zttpol2016_systematics as zttpol_systematics


class ZttPolarisationDatacards(object):
    ''' Datacard class for the polarisation analysis. '''

    def add_processes(self, channel, categories, bkg_processes, sig_processes=["ztt"], add_data=True, *args, **kwargs):
        ''' Add Observation and Process to the combine harvester instance. Uses the bin mapping from mapping_category2binid. '''
        bin = [(self._mapping_category2binid.get(channel, {}).get(category, 0), category) for category in categories]

        for key in ["channel", "procs", "bin", "signal"]:
            if key in kwargs:
                kwargs.pop(key)

        non_sig_kwargs = copy.deepcopy(kwargs)
        if "mass" in non_sig_kwargs:
            non_sig_kwargs.pop("mass")

        if add_data:
            self.cb.AddObservations(channel=[channel], mass=["*"], bin=bin, *args, **non_sig_kwargs)
        self.cb.AddProcesses(channel=[channel], mass=["*"], procs=bkg_processes, bin=bin, signal=False, *args, **non_sig_kwargs)
        self.cb.AddProcesses(channel=[channel], procs=sig_processes, bin=bin, signal=True, *args, **kwargs)


    def __init__(self, cb=None):
        super(ZttPolarisationDatacards, self).__init__()

        self.cb = cb

        self._mapping_category2binid = {
            "mt" : {

                "mt_a1" : 1010,
                "mt_rho" : 1020,
                "mt_oneprong" : 1030,
            },
            "et" : {

                "et_a1" : 1010,
                "et_rho" : 1020,
                "et_oneprong" : 1030,
            },
            "em" : {

                "em_oneprong" : 1030,
            },
            "tt" : {
                "tt_a1" : 1010,
                "tt_rho" : 1020,
                "tt_oneprong" : 1030,
            },
        }

        if self.cb is None:

            self.cb = ch.CombineHarvester()

            systematics = zttpol_systematics.SystematicLibary()

            # ======================================================================
            # MT channel
            self.add_processes(
                    channel="mt",
                    categories=["mt_"+category for category in ["rho", "oneprong", "a1", "a1_2", "rho_2", "oneprong_2", "oneprong_1",
                                                                "combined_a1_oneprong", "combined_rho_oneprong", "combined_oneprong_oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )

            # efficiencies
            self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics.muon_efficiency_syst_args)

            self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_efficiency_corr_syst_args)
            self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_es_syst_args)
            #self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_efficiency_syst_args)

            # from Yuta
            self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_scale_met_syst_args)
            self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_resolution_met_syst_args)
            self.cb.cp().channel(["mt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_scale_met_syst_args)
            self.cb.cp().channel(["mt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_resolution_met_syst_args)

            # extrapolation uncertainty
            self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_extrapol_syst_args)
            self.cb.cp().channel(["mt"]).process(["W"]).AddSyst(self.cb, *systematics.wj_extrapol_syst_args)

            # Tau ES
            self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_es_syst_args)

            # fake-rate
            self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics.eFakeTau_vloose_syst_args)
            self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics.muFakeTau_syst_args)
            self.cb.cp().channel(["mt"]).process(["ZJ"]).AddSyst(self.cb, *systematics.zjFakeTau_syst_args)

            # Top pT reweight
            #self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_syst_args)

            # ======================================================================
            # ET channel
            self.add_processes(
                    channel="et",
                    categories=["et_"+category for category in ["rho", "oneprong", "a1", "a1_2", "rho_2", "oneprong_2", "oneprong_1",
                                                                "combined_a1_oneprong", "combined_rho_oneprong", "combined_oneprong_oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )

            # efficiencies
            self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics.electron_efficiency_syst_args)

            self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_efficiency_corr_syst_args)
            self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_es_syst_args)
            #self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_efficiency_syst_args)

            # from Yuta
            self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_scale_met_syst_args)
            self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_resolution_met_syst_args)
            self.cb.cp().channel(["et"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_scale_met_syst_args)
            self.cb.cp().channel(["et"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_resolution_met_syst_args)

            # extrapolation uncertainty
            self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_extrapol_syst_args)
            self.cb.cp().channel(["et"]).process(["W"]).AddSyst(self.cb, *systematics.wj_extrapol_syst_args)

            # Tau ES
            self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_es_syst_args)

            # fake-rate
            self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics.eFakeTau_tight_syst_args)
            self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics.muFakeTau_syst_args)
            self.cb.cp().channel(["et"]).process(["ZJ"]).AddSyst(self.cb, *systematics.zjFakeTau_syst_args)

            # Top pT reweight
            #self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_syst_args)

            # ======================================================================
            # TT channel
            self.add_processes(
                    channel="tt",
                    categories=["tt_"+category for category in ["rho", "rho_1", "rho_2", "oneprong", "oneprong_1", "oneprong_2",
                                                                 "a1","a1_1","a1_2","combined_a1_a1","combined_a1_rho","combined_a1_oneprong",  "combined_oneprong_oneprong",
                                                                "combined_rho_rho","combined_rho_oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )

            # efficiencies
            self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_efficiency_corr_syst_args)
            self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_es_syst_args)
            #self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_efficiency_syst_args)

            # from Yuta
            self.cb.cp().channel(["tt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_scale_met_syst_args)
            self.cb.cp().channel(["tt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_resolution_met_syst_args)
            self.cb.cp().channel(["tt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_scale_met_syst_args)
            self.cb.cp().channel(["tt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_resolution_met_syst_args)

            # extrapolation uncertainty
            self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_extrapol_syst_args)
            self.cb.cp().channel(["tt"]).process(["W"]).AddSyst(self.cb, *systematics.wj_extrapol_syst_args)

            # Tau ES
            self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.tau_es_syst_args)

            # fake-rate
            self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, *systematics.eFakeTau_tight_syst_args)
            self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, *systematics.muFakeTau_syst_args)
            self.cb.cp().channel(["tt"]).process(["ZJ"]).AddSyst(self.cb, *systematics.zjFakeTau_syst_args)

            # Top pT reweight
            #self.cb.cp().channel(["tt"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_syst_args)

            # ======================================================================
            # EM channel
            self.add_processes(
                    channel="em",
                    categories=["em_"+category for category in ["oneprong"]],
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"],
                    mass=["0"]
            )

            # efficiencies
            self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics.electron_efficiency_syst_args)
            self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics.muon_efficiency_syst_args)

            # from Yuta
            self.cb.cp().channel(["em"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_scale_met_syst_args)
            self.cb.cp().channel(["em"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics.boson_resolution_met_syst_args)
            self.cb.cp().channel(["em"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_scale_met_syst_args)
            self.cb.cp().channel(["em"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics.ewk_top_resolution_met_syst_args)

            # extrapolation uncertainty
            self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_extrapol_syst_args)
            self.cb.cp().channel(["em"]).process(["W"]).AddSyst(self.cb, *systematics.wj_extrapol_syst_args)

            # Top pT reweight
            #self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics.ttj_syst_args)

            # ======================================================================
            # All channels
            #self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "ZTTPOSPOL_uniform_2", "ZTTNEGPOL_uniform_2", "lnU", ch.SystMap()(2.0))

            # lumi
            self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics.lumi_syst_args)

            # cross section
            self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ"]).AddSyst(self.cb, *systematics.zll_cross_section_syst_args)
            self.cb.cp().process(["VV"]).AddSyst(self.cb, *systematics.vv_cross_section_syst_args)
            self.cb.cp().process(["TT"]).AddSyst(self.cb, *systematics.ttj_cross_section_syst_args)
            self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics.wj_cross_section_syst_args)

            # signal acceptance/efficiency
            self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.ztt_pdf_scale_syst_args)
            self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics.ztt_qcd_scale_syst_args)

            # QCD systematic
            self.cb.cp().process(["QCD"]).AddSyst(self.cb, *systematics.qcd_syst_inclusive_args)

            # ======================================================================
            # Groups of systematics
            self.cb.SetGroup("syst", [".*"])
