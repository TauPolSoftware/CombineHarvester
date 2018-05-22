# -*- coding: utf-8 -*-

import logging
import copy
import re

import CombineHarvester.CombineTools.ch as ch


class ZttPolarisationDatacards(object):
    ''' Datacard class for the polarisation analysis. '''

    def add_processes(self, channel, categories, bkg_processes, sig_processes=["ztt"], add_data=True, *args, **kwargs):
        ''' Add Observation and Process to the combine harvester instance. Uses the bin mapping from mapping_category2binid. '''
        bin = [(self._mapping_category2binid.get(channel, {}).get(category, 0), category) for category in categories]

        for key in ["channel", "procs", "bin", "signal"]:
            if key in kwargs:
                kwargs.pop(key)

        if add_data:
            self.cb.AddObservations(channel=[channel], mass=["*"], bin=bin, *args, **kwargs)
        self.cb.AddProcesses(channel=[channel], mass=["*"], procs=bkg_processes, bin=bin, signal=False, *args, **kwargs)
        self.cb.AddProcesses(channel=[channel], mass=["*"], procs=sig_processes, bin=bin, signal=True, *args, **kwargs)


    def __init__(self, cb=None):
        super(ZttPolarisationDatacards, self).__init__()

        self.cb = cb

        self._mapping_category2binid = {
            "mt" : {
                "mt_inclusive" : 1000,
                
                "mt_a1" : 1010,
                "mt_rho" : 1020,
                "mt_oneprong" : 1030,

                "mt_combined_rho_oneprong" : 1040,
                "mt_combined_a1_oneprong" : 1050,
                "mt_combined_oneprong_oneprong" : 1060,

                "mt_a1_2" : 1012,
                "mt_rho_2" : 1022,
                "mt_oneprong_1" : 1031,
                "mt_oneprong_2" : 1032,

            },
            "et" : {
                "et_inclusive" : 1000,

                "et_a1" : 1010,
                "et_rho" : 1020,
                "et_oneprong" : 1030,

                "et_combined_rho_oneprong" : 1040,
                "et_combined_a1_oneprong" : 1050,
                "et_combined_oneprong_oneprong" : 1060,

                "et_a1_2" : 1012,
                "et_rho_2" : 1022,
                "et_oneprong_1" : 1031,
                "et_oneprong_2" : 1032,

            },
            "em" : {
                "em_inclusive" : 1000,

                "em_oneprong" : 1030,

                "em_oneprong_1" : 1031,
                "em_oneprong_2" : 1032,
                
                "em_combined_oneprong_oneprong" : 1060,
            },
            "tt" : {
                "tt_inclusive" : 1000,
                
                "tt_a1" : 1010,
                "tt_rho" : 1020,
                "tt_oneprong" : 1030,

                "tt_combined_rho_oneprong" : 1040,
                "tt_combined_a1_oneprong" : 1050,
                "tt_combined_oneprong_oneprong" : 1060,

                "tt_combined_a1_a1" : 1070,
                "tt_combined_a1_rho" : 1080,
                "tt_combined_rho_rho" : 1090,

                "tt_a1_1" : 1011,
                "tt_a1_2" : 1012,
                "tt_rho_1" : 1021,
                "tt_rho_2" : 1022,
                "tt_oneprong_1" : 1031,
                "tt_oneprong_2" : 1032,

            },
        }

        if self.cb is None:

            self.cb = ch.CombineHarvester()

            sig_procs = ["ZTTPOSPOL", "ZTTNEGPOL"]
            all_mc_bkgs_no_WQCD = ["ZLL", "ZL", "ZJ", "TT", "VV"]
            all_mc_bkgs = copy.deepcopy(all_mc_bkgs_no_WQCD)+["W", "QCD"]


            # ======================================================================
            # MT channel
            self.add_processes(
                    channel="mt",
                    categories=["mt_"+category for category in ["inclusive", "rho", "oneprong", "a1", "a1_2", "rho_2", "oneprong_2", "oneprong_1",
                                                                "combined_a1_oneprong", "combined_rho_oneprong", "combined_oneprong_oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"]
            )

            # efficiencies
            self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_m", "lnN", ch.SystMap("era")
                                                                                                                                                    (       ["13TeV"], 1.02))

            self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap("era", "channel")
                                                                                                                                   (["13TeV"], ["mt", "et", "tt"], 1.045))

            self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era", "channel")
                                                                                                                                            (["13TeV"], ["mt", "et", "tt"], 1.02))

            # Tau ID
            self.cb.cp().channel(["mt"]).process(sig_procs).bin_id([int(self._mapping_category2binid.get("mt", {}).get("mt_oneprong", 0))]).AddSyst(self.cb, "CMS_tauDMReco_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["mt"]).process(sig_procs).bin_id([int(self._mapping_category2binid.get("mt", {}).get("mt_rho", 0))]).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["mt"]).process(sig_procs).bin_id([int(self._mapping_category2binid.get("mt", {}).get("mt_a1", 0))]).AddSyst(self.cb, "CMS_tauDMReco_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))



            # extrapolation uncertainty
            self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                             (["13TeV"], ["TTJ", "TT"], 1.10))
            self.cb.cp().channel(["mt"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                           (       ["13TeV"], ["WJ", "W"], 1.2))

            # Tau ES
            self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("mt", {}).get("mt_oneprong", 0))]).AddSyst(self.cb,"CMS_scale_t_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("mt", {}).get("mt_rho", 0))]).AddSyst(self.cb,"CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("mt", {}).get("mt_a1", 0))]).AddSyst(self.cb,"CMS_scale_t_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))


            # fake-rate
            self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA", "lnN", ch.SystMap("era", "process", "channel")
                                                                                                                                      (       ["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10))
            self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_mFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)
                                                                                                                          (       ["13TeV"], ["ZLL", "ZL"], 2.00))
            self.cb.cp().channel(["mt"]).process(["ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)
                                                                                                                           (       ["13TeV"], ["ZLL", "ZL"], 1.30))
            self.cb.cp().channel(["mt"]).process( ["ZL"]).AddSyst(self.cb, "CMS_mFakeTau_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["mt"]).process( ["ZL"]).AddSyst(self.cb, "CMS_mFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))

            # Top pT reweight
            #self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")
            #                                                                                                            (["13TeV"], 1.0))

            # Trigger
            self.cb.cp().process(sig_procs +  all_mc_bkgs_no_WQCD).channel(["mt"]).AddSyst(self.cb,
                                         "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.02))

            # ======================================================================
            # ET channel
            self.add_processes(
                    channel="et",
                    categories=["et_"+category for category in ["inclusive", "rho", "oneprong", "a1", "a1_2", "rho_2", "oneprong_2", "oneprong_1",
                                                                "combined_a1_oneprong", "combined_rho_oneprong", "combined_oneprong_oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"]
            )

            # efficiencies
            self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_e", "lnN", ch.SystMap("era")
                                                                                                                                                    (       ["13TeV"], 1.02))

            self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap("era", "channel")
                                                                                                                                   (["13TeV"], ["mt", "et", "tt"], 1.045))

            self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era", "channel")
                                                                                                                                            (["13TeV"], ["mt", "et", "tt"], 1.02))
               
            # Tau ID
            self.cb.cp().channel(["et"]).process(sig_procs).bin_id([int(self._mapping_category2binid.get("et", {}).get("et_oneprong", 0))]).AddSyst(self.cb, "CMS_tauDMReco_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["et"]).process(sig_procs).bin_id([int(self._mapping_category2binid.get("et", {}).get("et_rho", 0))]).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["et"]).process(sig_procs).bin_id([int(self._mapping_category2binid.get("et", {}).get("et_a1", 0))]).AddSyst(self.cb, "CMS_tauDMReco_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))



            # extrapolation uncertainty
            self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                             (["13TeV"], ["TTJ", "TT"], 1.10))
            self.cb.cp().channel(["et"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                           (       ["13TeV"], ["WJ", "W"], 1.2))

            # Tau ES
            self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("et", {}).get("et_oneprong", 0))]).AddSyst(self.cb,"CMS_scale_t_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("et", {}).get("et_rho", 0))]).AddSyst(self.cb,"CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("et", {}).get("et_a1", 0))]).AddSyst(self.cb,"CMS_scale_t_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))

            # fake-rate
            self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA", "lnN", ch.SystMap("era", "process", "channel")
                                                                                                                                      (       ["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10))
            self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_mFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)
                                                                                                                          (       ["13TeV"], ["ZLL", "ZL"], 2.00))
            self.cb.cp().channel(["et"]).process(["ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)
                                                                                                                           (       ["13TeV"], ["ZLL", "ZL"], 1.30))
         
            self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_eFakeTau_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_eFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))


            # Top pT reweight
            #self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")
            #                                                                                                            (["13TeV"], 1.0))

            # Trigger
            self.cb.cp().process(sig_procs + all_mc_bkgs_no_WQCD).channel(["et"]).AddSyst(self.cb, "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.02))

            # ======================================================================
            # TT channel
            self.add_processes(
                    channel="tt",
                    categories=["tt_"+category for category in ["inclusive", "rho", "rho_1", "rho_2", "oneprong", "oneprong_1", "oneprong_2",
                                                                 "a1","a1_1","a1_2","combined_a1_a1","combined_a1_rho","combined_a1_oneprong",  "combined_oneprong_oneprong",
                                                                "combined_rho_rho","combined_rho_oneprong"]], # "a1"
                    bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"]
            )

            # efficiencies
            self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.09))

            self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.04))

            self.cb.cp().channel(["tt"]).process(["ZJ","W"]).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.06))

            self.cb.cp().channel(["tt"]).process(["ZJ","W"]).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.02))

            #self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era", "channel")
            #                                                                                                                              (["7TeV", "8TeV"], ["mt", "et"], 1.08)
            #                                                                                                                              (["7TeV", "8TeV"], ["tt"],       1.19)
            #                                                                                                                              (       ["13TeV"], ["mt", "et", "tt"], 1.03))

            # extrapolation uncertainty
            self.cb.cp().channel(["tt"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                             (["13TeV"], ["TTJ", "TT"], 1.10))
            self.cb.cp().channel(["tt"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                           (       ["13TeV"], ["WJ", "W"], 1.2))

            # Tau ES       
            self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("tt", {}).get("tt_oneprong", 0))]).AddSyst(self.cb,"CMS_scale_t_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("tt", {}).get("tt_rho", 0))]).AddSyst(self.cb,"CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
            self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).bin_id([int(self._mapping_category2binid.get("tt", {}).get("tt_a1", 0))]).AddSyst(self.cb,"CMS_scale_t_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
                            

            # fake-rate
            self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA", "lnN", ch.SystMap("era", "process", "channel")
                                                                                                                                      (       ["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10))
            self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_mFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)
                                                                                                                          (       ["13TeV"], ["ZLL", "ZL"], 2.00))
            self.cb.cp().channel(["tt"]).process(["ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)
                                                                                                                           (       ["13TeV"], ["ZLL", "ZL"], 1.30))

            # Top pT reweight
            #self.cb.cp().channel(["tt"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")
            #                                                                                                            (["13TeV"], 1.0))

            # Trigger
            self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.10))

            # ======================================================================
            # EM channel
            self.add_processes(
                    channel="em",
                    categories=["em_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_oneprong_oneprong"]],
                    bkg_processes=["ZLL", "TT", "VV", "W", "QCD"],
                    sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
                    analysis=["ztt"],
                    era=["13TeV"]
            )

            # efficiencies
            self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZLL", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_e", "lnN", ch.SystMap("era")
                                                                                                                                                    (       ["13TeV"], 1.02))
            self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZLL", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_m", "lnN", ch.SystMap("era")
                                                                                                                                                    (       ["13TeV"], 1.02))

            # extrapolation uncertainty
            self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                             (["13TeV"], ["TTJ", "TT"], 1.10))
            self.cb.cp().channel(["em"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                           (       ["13TeV"], ["WJ", "W"], 1.2))

            # Top pT reweight
            #self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")
            #                                                                                                            (["13TeV"], 1.0))

            # Trigger
            self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["em"]).AddSyst(self.cb,
                                         "CMS_eff_trigger_em_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.02))

            # ======================================================================
            # All channels
            #self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "ZTTPOSPOL_uniform_2", "ZTTNEGPOL_uniform_2", "lnU", ch.SystMap()(2.0))

            # lumi
            self.cb.cp().process(sig_procs + all_mc_bkgs_no_WQCD ).AddSyst(self.cb, "lumi_13TeV", "lnN", ch.SystMap("era")
                                                                                                                   (["13TeV"], 1.025))

            # cross section
            self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZLL", "ZL", "ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjXsec_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                                        (       ["13TeV"], ["ZLL", "ZL", "ZJ"], 1.04))
            self.cb.cp().process(["VV"]).AddSyst(self.cb, "CMS_$ANALYSIS_vvXsec_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                        (       ["13TeV"], ["VV", "VVT", "VVJ"], 1.10))
            self.cb.cp().process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjXsec_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                         (["13TeV"], ["TTJ", "TT", "TTT", "TTJJ"], 1.06))
            self.cb.cp().process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjXsec_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                       (       ["13TeV"], ["WJ", "W"], 1.04))

            # signal acceptance/efficiency
            self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "CMS_$ANALYSIS_pdf_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                         (["13TeV"], ["ZTT"], 1.015))
            self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "CMS_$ANALYSIS_QCDscale_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                                              (["13TeV"], ["ZTT"], 1.005))

            # QCD systematic
            self.cb.cp().process(["QCD"]).AddSyst(self.cb, "CMS_$ANALYSIS_qcdSyst_$ERA", "lnN", ch.SystMap("era", "process")
                                                                                                          (["13TeV"], ["QCD"], 1.10))

            # jet and met energy scale
            self.cb.cp().channel(["et","mt","tt","em"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_scale_met_clustered_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
            self.cb.cp().channel(["et","mt","tt","em"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_scale_met_unclustered_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))

            # ======================================================================
            # Groups of systematics
            #self.cb.SetGroup("syst", [".*"])

#===========================================================================================================================================================================================================================================
#===========================================================================================================================================================================================================================================
#===========================================================================================================================================================================================================================================

    def AddHTTSM2016Systematics(self):

        sig_procs = ["ZTTPOSPOL", "ZTTNEGPOL"]#["ggH_htt","qqH_htt","WH_htt","ZH_htt"]
        all_mc_bkgs = ["ZL","ZJ","TTJ","TTT","TT",
                       "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
                       "ggH_hww125","qqH_hww125","EWKZ"] #"ZTT"
        all_mc_bkgs_no_W = ["ZL","ZJ""TTJ","TTT","TT",
                            "ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
                            "ggH_hww125","qqH_hww125","EWKZ"] #"ZTT"
        all_mc_bkgs_no_TTJ = ["ZL","ZJ","TTT","TT",
                              "ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
                              "ggH_hww125","qqH_hww125","EWKZ"] #"ZTT"

        #~~~~~~~~~~~~~~~~~~~ Lumi ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.cb.cp().process(sig_procs + ["VV","VVT","VVJ","ggH_hww125","qqH_hww125"] ).AddSyst(self.cb,
                                    "lumi_13TeV", "lnN", ch.SystMap()(1.025))

        #Add luminosity uncertainty for W in em, tt, ttbar and the mm region as norm is from MC
        self.cb.cp().process(["W"]).channel(["tt","em","mm","ttbar"]).AddSyst(self.cb,
                                            "lumi_13TeV", "lnN", ch.SystMap()(1.025))

        #~~~~~~~~~~~~~~~~~~~ trigger ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.cb.cp().process(sig_procs +  all_mc_bkgs_no_W).channel(["mt"]).AddSyst(self.cb,
                                     "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.02))

        self.cb.cp().process(sig_procs + all_mc_bkgs_no_W).channel(["et"]).AddSyst(self.cb,
                                     "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.02))

        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["em","ttbar"]).AddSyst(self.cb,
                                     # hard coding channel here keeps "em" and "ttbar" correlated
                                     "CMS_eff_trigger_em_$ERA", "lnN", ch.SystMap()(1.02))

        #New
        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["tt"]).AddSyst(self.cb,
                                     "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.10))

        #~~~~~~~~~~~~~~~~~~~ Electron muon and tau id ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.cb.cp().AddSyst(self.cb, "CMS_eff_m", "lnN", ch.SystMap("channel", "process")
                             (["mm"], ["ZTT", "TT", "VV", "ZL", "ZJ"],  1.02)
                             (["mt"], sig_procs + all_mc_bkgs_no_W,  1.02)
                             (["em","ttbar"], sig_procs + all_mc_bkgs,  1.02))

        self.cb.cp().AddSyst(self.cb, "CMS_eff_e", "lnN", ch.SystMap("channel", "process")
                (["et"], sig_procs + all_mc_bkgs_no_W,  1.02)
                (["em","ttbar"], sig_procs + all_mc_bkgs,       1.02))


        # Tau Efficiency applied to all MC
        # in tautau channel the applied value depends on the number of taus which is determined by
        # gen match. WJets for example is assumed to have 1 real tau and 1 fake as is TTJ
        # compared to ZTT which has 2 real taus.
        # We also have channel specific components and fully correlated components
        #
        # ETau & MuTau
        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt"]).AddSyst(self.cb,
                                             "CMS_eff_t_$ERA", "lnN", ch.SystMap()(1.045))

        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt"]).AddSyst(self.cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.02))

        # TauTau - 2 real taus
        self.cb.cp().process(sig_procs + ["ZTT","VV","VVT","TTT","EWKZ"]).channel(["tt"]).AddSyst(self.cb,
                                             "CMS_eff_t_$ERA", "lnN", ch.SystMap()(1.09))

        self.cb.cp().process(sig_procs + ["ZTT","VV","VVT","TTT","EWKZ"]).channel(["tt"]).AddSyst(self.cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.04))

        # TauTau - 1+ jet to tau fakes
        self.cb.cp().process(["TTJ","ZJ","VVJ","W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest"]).channel(["tt"]).AddSyst(self.cb,
                                             "CMS_eff_t_$ERA", "lnN", ch.SystMap()(1.06))

        self.cb.cp().process(["TTJ","ZJ","VVJ","W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest"]).channel(["tt"]).AddSyst(self.cb,
                                             "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.02))




        ######################### Tau Id shape uncertainty (added March 08)

        self.cb.cp().channel(["et","mt"]).process(["ZTT"]).bin_id([1]).AddSyst(self.cb, "CMS_tauDMReco_1prong_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().channel(["et","mt"]).process(["ZTT"]).bin_id([1]).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().channel(["et","mt"]).process(["ZTT"]).bin_id([1]).AddSyst(self.cb, "CMS_tauDMReco_3prong_$ERA", "shape", ch.SystMap()(1.00))


        #~~~~~~~~~~~~~~~~~~~ b tag and mistag rate  efficiencies ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.cb.cp().AddSyst(self.cb, "CMS_htt_eff_b_$ERA", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"], [1], ["TTJ","TTT","TT"], 1.035))
        self.cb.cp().AddSyst(self.cb, "CMS_htt_eff_b_$ERA", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"], [2,3], ["TTJ","TTT","TT"], 1.05))

        self.cb.cp().AddSyst(self.cb, "CMS_htt_eff_b_$ERA", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"], [2,3], ["VV","VVT","VVJ"], 1.015))  # Mainly SingleTop

        #~~~~~~~~~~~~~~~~~~~ Electron and tau energy Scale ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.cb.cp().process(sig_procs + all_mc_bkgs + ["QCD"]).channel(["em"]).AddSyst(self.cb,
                                             "CMS_scale_e_$CHANNEL_$ERA", "shape", ch.SystMap()(1.00))

        # Decay Mode based TES Settings
        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt","tt"]).AddSyst(self.cb,
                                                  "CMS_scale_t_1prong_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt","tt"]).AddSyst(self.cb,
                                                  "CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt","tt"]).AddSyst(self.cb,
                                                  "CMS_scale_t_3prong_$ERA", "shape", ch.SystMap()(1.00))

        #~~~~~~~~~~~~~~~~~~~ jet and met energy Scale ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # MET Systematic shapes
        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt","tt","em"]).bin_id([1,2,3]).AddSyst(self.cb,
                                                  "CMS_scale_met_clustered_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt","tt","em"]).bin_id([1,2,3]).AddSyst(self.cb,
                                                  "CMS_scale_met_unclustered_$ERA", "shape", ch.SystMap()(1.00))


        #        cb.cp().AddSyst(self.cb,
        #                        "CMS_htt_scale_met_$ERA", "lnN", ch.SystMap(channel, bin_id, process")
        #                        (["et", "mt", "em", "tt","ttbar"], [1, 2, 3], sig_procs + , all_mc_bkgs_no_W}), 1.01))
        self.cb.cp().AddSyst(self.cb,
                        "CMS_htt_scale_met_$ERA", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["ttbar"], [1, 2, 3], all_mc_bkgs, 1.01))

        #if (control_region > 0):
        #    # Add to all CRs, don't include QCD or WJets in et/mt which have CRs, or QCD in tt

        #    self.cb.cp().process(all_mc_bkgs).channel(["et","mt"]).bin_id([10, 11, 12, 13, 14, 15]).AddSyst(self.cb,
        #                                                    "CMS_scale_met_clustered_$ERA", "shape", ch.SystMap()(1.00))
        #    self.cb.cp().process(all_mc_bkgs).channel(["et","mt"]).bin_id([10, 11, 12, 13, 14, 15]).AddSyst(self.cb,
        #                                                    "CMS_scale_met_unclustered_$ERA", "shape", ch.SystMap()(1.00))


        #            cb.cp().AddSyst(self.cb,
        #                            "CMS_htt_scale_met_$ERA", "lnN", ch.SystMap(channel, bin_id, process")
        #                            (["et", "mt"], [10, 11, 12, 13, 14, 15], JoinStr({all_mc_bkgs_no_W}), 1.01))
        #            cb.cp().AddSyst(self.cb,
        #                            "CMS_htt_scale_met_$ERA", "lnN", ch.SystMap(channel, bin_id, process")
        #                            (["tt"], {10, 11, 12}, JoinStr(all_mc_bkgs), 1.01))






        #~~~~~~~~~~~~~~~~~~~ Background normalization uncertainties ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #   Diboson  Normalisation - fully correlated
        self.cb.cp().process(["VV","VVT","VVJ","VVJ_rest"]).AddSyst(self.cb,
                                        "CMS_htt_vvXsec_13TeV", "lnN", ch.SystMap()(1.05))
        #if (not  ttbar_fit):
        #    #   ttbar Normalisation - fully correlated
        #    self.cb.cp().process(["TT","TTT","TTJ","TTJ_rest"]).AddSyst(self.cb,
        #                  "CMS_htt_tjXsec_13TeV", "lnN", ch.SystMap()(1.06))

        # W norm, just for em, tt and the mm region where MC norm is from MC
        #        cb.cp().process(["W","W_rest"]).channel(["tt","em","mm"]).AddSyst(self.cb,
        #                                             "CMS_htt_wjXsec_13TeV", "lnN", ch.SystMap()(1.20))  # splitted to two uncertainties as following

        self.cb.cp().process(["W"]).channel(["em"]).AddSyst(self.cb,
                                                       "CMS_htt_jetFakeLep_13TeV", "lnN", ch.SystMap()(1.20))

        self.cb.cp().process(["W"]).channel(["tt"]).AddSyst(self.cb,
                                                       "CMS_htt_wjXsec_13TeV", "lnN", ch.SystMap()(1.04))


        # QCD norm, just for em  decorrelating QCD BG for differenet categories
        #        cb.cp().process(["QCD"]).channel(["em"]).AddSyst(self.cb,
        #
        #                                           "CMS_htt_QCD_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.20))

        # QCD norm, just for tt
        self.cb.cp().process(["QCD"]).channel(["em"]).bin_id([1]).AddSyst(self.cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.10))
        self.cb.cp().process(["QCD"]).channel(["em"]).bin_id([2]).AddSyst(self.cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.10))
        self.cb.cp().process(["QCD"]).channel(["em"]).bin_id([3]).AddSyst(self.cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.20))


        # QCD norm, just for tt
        self.cb.cp().process(["QCD"]).channel(["tt"]).bin_id([1]).AddSyst(self.cb,
                                             "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.027))
        self.cb.cp().process(["QCD"]).channel(["tt"]).bin_id([2]).AddSyst(self.cb,
                                             "CMS_htt_QCD_boosted_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.027))
        self.cb.cp().process(["QCD"]).channel(["tt"]).bin_id([3]).AddSyst(self.cb,
                                             "CMS_htt_QCD_VBF_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.15))


        #Iso to antiiso extrapolation
        self.cb.cp().process(["QCD"]).channel(["mt"]).bin_id([1,2,3]).AddSyst(self.cb,
                                             "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.20))
        self.cb.cp().process(["QCD"]).channel(["et"]).bin_id([1,2,3]).AddSyst(self.cb,
                                             "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.20))


        #This should affect only shape (normalized to nominal values)
        self.cb.cp().process(["QCD"]).channel(["et","mt"]).bin_id([1]).AddSyst(self.cb,
                                             "WSFUncert_$CHANNEL_0jet_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["QCD"]).channel(["et","mt"]).bin_id([2]).AddSyst(self.cb,
                                             "WSFUncert_$CHANNEL_boosted_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["QCD"]).channel(["et","mt"]).bin_id([3]).AddSyst(self.cb,
                                             "WSFUncert_$CHANNEL_vbf_$ERA", "shape", ch.SystMap()(1.00))


        # based on the Ersatz study in Run1
        self.cb.cp().process(["W"]).channel(["et","mt"]).bin_id([1]).AddSyst(self.cb,
                                             "WHighMTtoLowMT_0jet_$ERA", "lnN", ch.SystMap()(1.10))
        self.cb.cp().process(["W"]).channel(["et","mt"]).bin_id([2]).AddSyst(self.cb,
                                             "WHighMTtoLowMT_boosted_$ERA", "lnN", ch.SystMap()(1.05))
        self.cb.cp().process(["W"]).channel(["et","mt"]).bin_id([3]).AddSyst(self.cb,
                                             "WHighMTtoLowMT_vbf_$ERA", "lnN", ch.SystMap()(1.10))



        #~~~~~~~~~~~~~~~~~~~ DY LO.NLO reweighting, Between no and twice the correc(on. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.cb.cp().process( ["ZTT","ZJ","ZL","ZJ_rest"]).channel(["et","mt","tt"]).AddSyst(self.cb,
                                             "CMS_htt_dyShape_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process( ["ZTT","ZL"]).channel(["em"]).AddSyst(self.cb,
                                             "CMS_htt_dyShape_$ERA", "shape", ch.SystMap()(1.00))

        #~~~~~~~~~~~~~~~~~~~ Ttbar shape reweighting, Between no and twice the correction ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.cb.cp().process( ["TTJ","TTT","TTJ_rest"]).channel(["tt"]).AddSyst(self.cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process( ["TTJ","TTT"]).channel(["et","mt"]).AddSyst(self.cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process( ["tt"]).channel(["em"]).AddSyst(self.cb,
                                        "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap()(1.00))

        #~~~~~~~~~~~~~~~~~~~ ZL shape  and electron/muon  to tau fake only in  mt and et channels (updated March 22) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.cb.cp().process( ["ZL"]).channel(["mt","et"]).AddSyst(self.cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process( ["ZL"]).channel(["mt","et"]).AddSyst(self.cb,
                                                         "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
        #Changed March 10
        #        cb.cp().process(["ZL"]).channel(["mt"]).AddSyst(self.cb,
        #                                                        "CMS_htt_mFakeTau_13TeV", "lnN", ch.SystMap()(1.25))
        #        cb.cp().process(["ZL"]).channel(["et"]).AddSyst(self.cb,
        #                                                        "CMS_htt_eFakeTau_13TeV", "lnN", ch.SystMap()(1.12))


        self.cb.cp().process( ["ZL"]).channel(["mt"]).bin_id([1,2,3]).AddSyst(self.cb,
                                                                     "CMS_mFakeTau_1prong_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process( ["ZL"]).channel(["mt"]).bin_id([1,2,3]).AddSyst(self.cb,
                                                                     "CMS_mFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process( ["ZL"]).channel(["et"]).bin_id([1,2,3]).AddSyst(self.cb,
                                                                     "CMS_eFakeTau_1prong_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process( ["ZL"]).channel(["et"]).bin_id([1,2,3]).AddSyst(self.cb,
                                                                     "CMS_eFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))

        #
        #        cb.cp().process( ["ZL"]).channel(["mt"]).bin_id([1]).AddSyst(self.cb,
        #                                                                        "CMS_ZLShape_mFakeTau_0jet_1prong_$ERA", "shape", ch.SystMap()(1.00))
        #        cb.cp().process( ["ZL"]).channel(["mt"]).bin_id([1]).AddSyst(self.cb,
        #                                                                        "CMS_ZLShape_mFakeTau_0jet_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
        #        cb.cp().process( ["ZL"]).channel(["et"]).bin_id([1]).AddSyst(self.cb,
        #                                                                        "CMS_ZLShape_eFakeTau_0jet_1prong_$ERA", "shape", ch.SystMap()(1.00))
        #        cb.cp().process( ["ZL"]).channel(["et"]).bin_id([1]).AddSyst(self.cb,
        #                                                                        "CMS_ZLShape_eFakeTau_0jet_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
        #

        #~~~~~~~~~~~~~~~~~~~ jet  to tau fake only in tt, mt and et channels ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.cb.cp().process( ["TTJ","ZJ","VVJ","W_rest","ZJ_rest","TTJ_rest","VVJ_rest"]).channel(["tt","mt","et"]).AddSyst(self.cb,
                                                                            "CMS_htt_jetToTauFake_$ERA", "shape", ch.SystMap()(1.00))

        self.cb.cp().process( ["W"]).channel(["tt","mt","et"]).bin_id([1,2,3,13,14,15]).AddSyst(self.cb,
                                                                "CMS_htt_jetToTauFake_$ERA", "shape", ch.SystMap()(1.00))

    
