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
        self.cb.cp().process(["W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest"]).channel(["tt"]).AddSyst(self.cb,"lumi_13TeV", "lnN", ch.SystMap()(1.025))

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

        self.cb.cp().process(["ZTT"]).channel(["et","mt"]).bin_id([1]).AddSyst(self.cb,
                                                            "CMS_tauDMReco_1prong_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["ZTT"]).channel(["et","mt"]).bin_id([1]).AddSyst(self.cb,
                                                                          "CMS_tauDMReco_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["ZTT"]).channel(["et","mt"]).bin_id([1]).AddSyst(self.cb,
                                                                          "CMS_tauDMReco_3prong_$ERA", "shape", ch.SystMap()(1.00))


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

        # Use only one of the TES options below per channel
        # these both need to be included while we work on getting all channels
        # having DM based TES, then we will switch permanently
        #
        # Standard TES
        # FIXME
        # This CR segment is temporary, just to check that the CRs work (needed to use old DCS
        # without scale_t on all shapes)
        # FIXME
        #        if (control_region == 1) {
        #            cb.cp().process(sig_procs + , ["ZTT","TTT","VV","VVT","EWKZ"]})).channel(["et","mt","tt"]).AddSyst(self.cb,
        #                                             "CMS_scale_t_$CHANNEL_$ERA", "shape", ch.SystMap()(1.00))
        #        }
        #        else {
        #            cb.cp().process(sig_procs + all_mc_bkgs).channel(["et","mt","tt"]).AddSyst(self.cb,
        #                                             "CMS_scale_t_$CHANNEL_$ERA", "shape", ch.SystMap()(1.00))
        #        }


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

        #~~~~~~~~~~~~~~~~~~~ Theoretical Uncertainties on signal ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #scale_gg on signal
        self.cb.cp().process( ["ggH_htt"]).channel(["et","mt","tt","em"]).AddSyst(self.cb,
                                             "CMS_scale_gg_$ERA", "shape", ch.SystMap()(1.00))

        # Scale uncertainty on signal Applies to ggH in boosted and VBF. Event-by-event weight applied as a func(on of pth or mjj. Fully correlated between categories and final states.


        # Covered by CMS_scale_gg above
        #cb.cp().AddSyst(self.cb, "CMS_ggH_QCDUnc", "lnN", ch.SystMap(channel, bin_id, process")
        #                (["em"],[1],["ggH_htt"], 0.93)
        #                (["et"],[1],["ggH_htt"], 0.93)
        #                (["mt"],[1],["ggH_htt"], 0.93)
        #                (["tt"],[1],["ggH_htt"], 0.93)
        #
        #                (["em"],[2],["ggH_htt"], 1.15)
        #                (["et"],[2],["ggH_htt"], 1.18)
        #                (["mt"],[2],["ggH_htt"], 1.18)
        #                (["tt"],[2],["ggH_htt"], 1.20)
        #
        #
        #                (["em"],[3],["ggH_htt"], 1.25)
        #                (["et"],[3],["ggH_htt"], 1.15)
        #                (["mt"],[3],["ggH_htt"], 1.08)
        #                (["tt"],[3],["ggH_htt"], 1.10)
        #                )



        self.cb.cp().AddSyst(self.cb, "CMS_qqH_QCDUnc", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["qqH_htt"], 0.997)
                        (["et"],[1],["qqH_htt"], 1.003)
                        (["mt"],[1],["qqH_htt"], 0.998)
                        (["tt"],[1],["qqH_htt"], 0.997)

                        (["em"],[2],["qqH_htt"], 1.004)
                        (["et"],[2],["qqH_htt"], 1.004)
                        (["mt"],[2],["qqH_htt"], 1.002)
                        (["tt"],[2],["qqH_htt"], 1.003)


                        (["em"],[3],["qqH_htt"], 1.005)
                        (["et"],[3],["qqH_htt"], 1.005)
                        (["mt"],[3],["qqH_htt"], 1.002)
                        (["tt"],[3],["qqH_htt"], 1.003)
                        )




        self.cb.cp().AddSyst(self.cb, "CMS_ggH_PDF", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["ggH_htt"], 1.007)
                        (["et"],[1],["ggH_htt"], 1.007)
                        (["mt"],[1],["ggH_htt"], 1.007)
                        (["tt"],[1],["ggH_htt"], 1.009)

                        (["em"],[2],["ggH_htt"], 1.007)
                        (["et"],[2],["ggH_htt"], 1.007)
                        (["mt"],[2],["ggH_htt"], 1.007)
                        (["tt"],[2],["ggH_htt"], 1.009)


                        (["em"],[3],["ggH_htt"], 1.007)
                        (["et"],[3],["ggH_htt"], 1.007)
                        (["mt"],[3],["ggH_htt"], 1.007)
                        (["tt"],[3],["ggH_htt"], 1.009)
                        )



        self.cb.cp().AddSyst(self.cb, "CMS_qqH_PDF", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["qqH_htt"], 1.011)
                        (["et"],[1],["qqH_htt"], 1.005)
                        (["mt"],[1],["qqH_htt"], 1.005)
                        (["tt"],[1],["qqH_htt"], 1.008)

                        (["em"],[2],["qqH_htt"], 1.005)
                        (["et"],[2],["qqH_htt"], 1.002)
                        (["mt"],[2],["qqH_htt"], 1.002)
                        (["tt"],[2],["qqH_htt"], 1.003)


                        (["em"],[3],["qqH_htt"], 1.005)
                        (["et"],[3],["qqH_htt"], 1.005)
                        (["mt"],[3],["qqH_htt"], 1.005)
                        (["tt"],[3],["qqH_htt"], 1.005)
                        )




        self.cb.cp().AddSyst(self.cb, "CMS_ggH_UEPS", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["ggH_htt"], 1.015)
                        (["et"],[1],["ggH_htt"], 1.015)
                        (["mt"],[1],["ggH_htt"], 1.015)
                        (["tt"],[1],["ggH_htt"], 1.015)

                        (["em"],[2],["ggH_htt"], 0.945)
                        (["et"],[2],["ggH_htt"], 0.945)
                        (["mt"],[2],["ggH_htt"], 0.945)
                        (["tt"],[2],["ggH_htt"], 0.945)

                        (["em"],[3],["ggH_htt"], 1.03)
                        (["et"],[3],["ggH_htt"], 1.03)
                        (["mt"],[3],["ggH_htt"], 1.03)
                        (["tt"],[3],["ggH_htt"], 1.03)
                        )



        self.cb.cp().AddSyst(self.cb, "CMS_qqH_UEPS", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["qqH_htt"], 1.015)
                        (["et"],[1],["qqH_htt"], 1.015)
                        (["mt"],[1],["qqH_htt"], 1.015)
                        (["tt"],[1],["qqH_htt"], 1.015)

                        (["em"],[2],["qqH_htt"], 0.945)
                        (["et"],[2],["qqH_htt"], 0.945)
                        (["mt"],[2],["qqH_htt"], 0.945)
                        (["tt"],[2],["qqH_htt"], 0.945)

                        (["em"],[3],["qqH_htt"], 1.03)
                        (["et"],[3],["qqH_htt"], 1.03)
                        (["mt"],[3],["qqH_htt"], 1.03)
                        (["tt"],[3],["qqH_htt"], 1.03)
                        )



        #cb.cp().AddSyst(self.cb, "CMS_ggH_mcComp", "lnN", ch.SystMap(channel, bin_id, process")
        #                (["em"],[1],["ggH_htt"], 0.95)
        #                (["et"],[1],["ggH_htt"], 0.95)
        #                (["mt"],[1],["ggH_htt"], 0.95)
        #                (["tt"],[1],["ggH_htt"], 0.95)
        #
        #                (["em"],[2],["ggH_htt"], 1.15)
        #                (["et"],[2],["ggH_htt"], 1.15)
        #                (["mt"],[2],["ggH_htt"], 1.15)
        #                (["tt"],[2],["ggH_htt"], 1.15)
        #                (["em"],[3],["ggH_htt"], 1.20)
        #                (["et"],[3],["ggH_htt"], 1.10)
        #                (["mt"],[3],["ggH_htt"], 1.10)
        #                (["tt"],[3],["ggH_htt"], 1.10)
        #                )



        #cb.cp().AddSyst(self.cb, "CMS_qqH_mcComp", "lnN", ch.SystMap(channel, bin_id, process")
        #                (["em"],[1],["qqH_htt"], 0.95)
        #                (["et"],[1],["qqH_htt"], 0.95)
        #                (["mt"],[1],["qqH_htt"], 1.05)
        #                (["tt"],[1],["qqH_htt"], 1.05)
        #
        #                (["em"],[2],["qqH_htt"], 1.10)
        #                (["et"],[2],["qqH_htt"], 1.10)
        #                (["mt"],[2],["qqH_htt"], 1.10)
        #                (["tt"],[2],["qqH_htt"], 1.05)
        #
        #                (["em"],[3],["qqH_htt"], 0.90)
        #                (["et"],[3],["qqH_htt"], 0.90)
        #                (["mt"],[3],["qqH_htt"], 0.90)
        #                (["tt"],[3],["qqH_htt"], 0.90)
        #                )


        #    Uncertainty on BR for HTT @ 125 GeV
        self.cb.cp().process(sig_procs).AddSyst(self.cb,"BR_htt_THU", "lnN", ch.SystMap()(1.017))
        self.cb.cp().process(sig_procs).AddSyst(self.cb,"BR_htt_PU_mq", "lnN", ch.SystMap()(1.0099))
        self.cb.cp().process(sig_procs).AddSyst(self.cb,"BR_htt_PU_alphas", "lnN", ch.SystMap()(1.0062))

        #    Uncertainty on BR of HWW @ 125 GeV
        self.cb.cp().process(["ggH_hww125","qqH_hww125"]).AddSyst(self.cb,"BR_hww_THU", "lnN", ch.SystMap()(1.0099))
        self.cb.cp().process(["ggH_hww125","qqH_hww125"]).AddSyst(self.cb,"BR_hww_PU_mq", "lnN", ch.SystMap()(1.0099))
        self.cb.cp().process(["ggH_hww125","qqH_hww125"]).AddSyst(self.cb,"BR_hww_PU_alphas", "lnN", ch.SystMap()(1.0066))


        self.cb.cp().process(["ggH_htt","ggH_hww125"]).AddSyst(self.cb,"QCDScale_ggH", "lnN", ch.SystMap()(1.039))
        self.cb.cp().process(["qqH_htt","qqH_hww125"]).AddSyst(self.cb,"QCDScale_qqH", "lnN", ch.SystMap()(1.004))
        self.cb.cp().process(["WH_htt"]).AddSyst(self.cb,"QCDScale_VH", "lnN", ch.SystMap()(1.007))
        self.cb.cp().process(["ZH_htt"]).AddSyst(self.cb,"QCDScale_VH", "lnN", ch.SystMap()(1.038))

        self.cb.cp().process(["ggH_htt","ggH_hww125"]).AddSyst(self.cb,"pdf_Higgs_gg", "lnN", ch.SystMap()(1.032))
        self.cb.cp().process(["qqH_htt","qqH_hww125"]).AddSyst(self.cb,"pdf_Higgs_qq", "lnN", ch.SystMap()(1.021))
        self.cb.cp().process(["WH_htt"]).AddSyst(self.cb,"pdf_Higgs_VH", "lnN", ch.SystMap()(1.019))
        self.cb.cp().process(["ZH_htt"]).AddSyst(self.cb,"pdf_Higgs_VH", "lnN", ch.SystMap()(1.016))







        #   Additonal uncertainties applied to the paper i.e. top mass
        self.cb.cp().process( ["ggH_htt"]).channel(["et","mt","em","tt"]).AddSyst(self.cb,
                                                                         "TopMassTreatment_$ERA", "shape", ch.SystMap()(1.00))


        self.cb.cp().AddSyst(self.cb, "CMS_ggH_STXSmig01", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["ggH_htt"], 0.959)
                        (["et"],[1],["ggH_htt"], 0.959)
                        (["mt"],[1],["ggH_htt"], 0.959)
                        (["tt"],[1],["ggH_htt"], 0.959)

                        (["em"],[2],["ggH_htt"], 1.079)
                        (["et"],[2],["ggH_htt"], 1.079)
                        (["mt"],[2],["ggH_htt"], 1.079)
                        (["tt"],[2],["ggH_htt"], 1.079)

                        (["em"],[3],["ggH_htt"], 1.039)
                        (["et"],[3],["ggH_htt"], 1.039)
                        (["mt"],[3],["ggH_htt"], 1.039)
                        (["tt"],[3],["ggH_htt"], 1.039)
                        )


        self.cb.cp().AddSyst(self.cb, "CMS_ggH_STXSmig12", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["ggH_htt"], 1.000)
                        (["et"],[1],["ggH_htt"], 1.000)
                        (["mt"],[1],["ggH_htt"], 1.000)
                        (["tt"],[1],["ggH_htt"], 1.000)

                        (["em"],[2],["ggH_htt"], 0.932)
                        (["et"],[2],["ggH_htt"], 0.932)
                        (["mt"],[2],["ggH_htt"], 0.932)
                        (["tt"],[2],["ggH_htt"], 0.932)

                        (["em"],[3],["ggH_htt"], 1.161)
                        (["et"],[3],["ggH_htt"], 1.161)
                        (["mt"],[3],["ggH_htt"], 1.161)
                        (["tt"],[3],["ggH_htt"], 1.161)
                        )

        self.cb.cp().AddSyst(self.cb, "CMS_ggH_STXSVBF2j", "lnN", ch.SystMap("channel", "bin_id", "process")
                        (["em"],[1],["ggH_htt"], 1.000)
                        (["et"],[1],["ggH_htt"], 1.000)
                        (["mt"],[1],["ggH_htt"], 1.000)
                        (["tt"],[1],["ggH_htt"], 1.000)

                        (["em"],[2],["ggH_htt"], 1.000)
                        (["et"],[2],["ggH_htt"], 1.000)
                        (["mt"],[2],["ggH_htt"], 1.000)
                        (["tt"],[2],["ggH_htt"], 1.000)

                        (["em"],[3],["ggH_htt"], 1.200)
                        (["et"],[3],["ggH_htt"], 1.200)
                        (["mt"],[3],["ggH_htt"], 1.200)
                        (["tt"],[3],["ggH_htt"], 1.200)
                        )


        #if control_region == 1:
        #    # Create rateParams for control regions:
        #    #  - [x] 1 rateParam for all W in every region
        #    #  - [x] 1 rateParam for QCD in low mT
        #    #  - [x] 1 rateParam for QCD in high mT
        #    #  - [x] lnNs for the QCD OS/SS ratio
        #    #         * should account for stat + syst
        #    #         * systs should account for: extrap. from anti-iso to iso region,
        #    #           possible difference between ratio in low mT and high mT (overkill?)
        #    #  - [x] lnNs for the W+jets OS/SS ratio
        #    #         * should account for stat only if not being accounted for with bbb,
        #    #           i.e. because the OS/SS ratio was measured with a relaxed selection
        #    #         * systs should account for: changes in low/high mT and OS/SS due to JES
        #    #           and btag (if relevant)  OS/SS being wrong in the MC (from enriched data?)
        #    #           low/high mT being wrong in the MC (fake rate dependence?)

        #    # Going to use the regex filtering to select the right subset of
        #    # categories for each rateParam
        #    self.cb.SetFlag("filters-use-regex", true)
        #    #      for (auto bin : cb_sig.cp().channel(["et", "mt"]).bin_set()) {
        #    # Regex that matches, e.g. mt_nobtag or mt_nobtag_X



        #    self.cb.cp().bin(["mt_0jet","mt_wjets_0jet_cr"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_0jet_mt", "rateParam", ch.SystMap()(1.0))
        #    self.cb.cp().bin(["mt_boosted","mt_wjets_boosted_cr","mt_vbf"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_boosted_mt", "rateParam", ch.SystMap()(1.0))
        #    #            cb.cp().bin(["mt_vbf","mt_wjets_vbf_cr"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_vbf_mt", "rateParam", ch.SystMap()(1.0))

        #    self.cb.cp().bin(["et_0jet","et_wjets_0jet_cr"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_0jet_et", "rateParam", ch.SystMap()(1.0))
        #    self.cb.cp().bin(["et_boosted","et_wjets_boosted_cr","et_vbf"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_boosted_et", "rateParam", ch.SystMap()(1.0))
        #    #            cb.cp().bin(["et_vbf","et_wjets_vbf_cr"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_vbf_et", "rateParam", ch.SystMap()(1.0))


        #    self.cb.cp().bin(["mt_0jet","mt_antiiso_0jet_cr"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_0jet_mt", "rateParam", ch.SystMap()(1.0))
        #    self.cb.cp().bin(["mt_boosted","mt_antiiso_boosted_cr","mt_vbf"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_boosted_mt", "rateParam", ch.SystMap()(1.0))
        #    #            cb.cp().bin(["mt_vbf","mt_antiiso_vbf_cr"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_vbf_mt", "rateParam", ch.SystMap()(1.0))

        #    self.cb.cp().bin(["et_0jet","et_antiiso_0jet_cr"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_0jet_et", "rateParam", ch.SystMap()(1.0))
        #    self.cb.cp().bin(["et_boosted","et_antiiso_boosted_cr","et_vbf"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_boosted_et", "rateParam", ch.SystMap()(1.0))
        #    #            cb.cp().bin(["et_vbf","et_antiiso_vbf_cr"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_vbf_et", "rateParam", ch.SystMap()(1.0))


        #    #          cb.cp().bin({bin+"(|_0jet)$"]).process(["W"]).AddSyst(self.cb, "rate_QCD_cr_0jet_"+bin, "rateParam", ch.SystMap()(1.0))
        #    #          cb.cp().bin({bin+"(|_boosted)$"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_1jet_"+bin, "rateParam", ch.SystMap()(1.0))
        #    #          cb.cp().bin({bin+"(|_vbf)$"]).process(["W"]).AddSyst(self.cb, "rate_W_cr_vbf_"+bin, "rateParam", ch.SystMap()(1.0))

        #    self.cb.cp().bin(["tt_0jet","tt_0jet_qcd_cr"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_0jet_tt", "rateParam", ch.SystMap()(1.0))
        #    self.cb.cp().bin(["tt_boosted","tt_boosted_qcd_cr"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_boosted_tt", "rateParam", ch.SystMap()(1.0))
        #    self.cb.cp().bin(["tt_vbf","tt_vbf_qcd_cr"]).process(["QCD"]).AddSyst(self.cb, "rate_QCD_cr_vbf_tt", "rateParam", ch.SystMap()(1.0))


        #    #        cb.cp().bin({bin+"(|_.*)$"]).process(["W"]).AddSyst(self.cb,
        #    #          "rate_W_cr_"+bin, "rateParam", ch.SystMap()(1.0))
        #    #
        #    #        # Regex that matches, e.g. mt_nobtag or mt_nobtag_qcd_cr
        #    #        cb.cp().bin({bin+"(|_antiiso_)$"]).process(["QCD"]).AddSyst(self.cb,
        #    #          "rate_QCD_antiiso_"+bin, "rateParam", ch.SystMap()(1.0))

        #    # Regex that matches, e.g. mt_nobtag_wjets_cr or mt_nobtag_wjets_ss_cr
        #    #        cb.cp().bin({bin+"_wjets_$"]).process(["QCD"]).AddSyst(self.cb,
        #    #          "rate_QCD_highmT_"+bin, "rateParam", ch.SystMap()(1.0))
        #    #      }

        #    ########/
        #    # Systematics #
        #    ########/


        #    # Should set a sensible range for our rateParams
        #    for sys in cb.cp().syst_type(["rateParam"]).syst_name_set():
        #                        cb.GetParameter(sys).set_range(0.0, 5.0)

        #    self.cb.SetFlag("filters-use-regex", false)


        #if (ttbar_fit):
        #        cb.SetFlag("filters-use-regex", true)

        #        self.cb.cp().bin(["mt_0jet"]).process(["TTJ","TTT"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["et_0jet"]).process(["TTJ","TTT"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["tt_0jet"]).process(["TTJ","TTT","TTJ_rest"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["em_0jet"]).process(["tt"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))


        #        self.cb.cp().bin(["mt_boosted"]).process(["TTJ","TTT"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["et_boosted"]).process(["TTJ","TTT"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["tt_boosted"]).process(["TTJ","TTT","TTJ_rest"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["em_boosted"]).process(["tt"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))


        #        self.cb.cp().bin(["mt_vbf"]).process(["TTJ","TTT"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["et_vbf"]).process(["TTJ","TTT"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["tt_vbf"]).process(["TTJ","TTT","TTJ_rest"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
        #        self.cb.cp().bin(["em_vbf"]).process(["tt"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))

        #        self.cb.cp().bin(["ttbar_all"]).process(["tt"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))

        #        self.cb.GetParameter("rate_ttbar").set_range(0.80, 1.20)

        #        self.cb.SetFlag("filters-use-regex", false)

        #jet fakes: shape uncertainties
        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_norm_ff_qcd_1prong_njet0_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_norm_ff_qcd_1prong_njet1_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_norm_ff_qcd_3prong_njet0_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_norm_ff_qcd_3prong_njet1_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))

        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_w_1prong_njet0_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_w_1prong_njet1_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_w_3prong_njet0_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_w_3prong_njet1_$CHANNEL_stat_13TeV", "shape", ch.SystMap()(1.00))

        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_tt_1prong_njet0_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_tt_1prong_njet1_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_tt_3prong_njet0_stat_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_tt_3prong_njet1_stat_13TeV", "shape", ch.SystMap()(1.00))

        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_norm_ff_qcd_$CHANNEL_syst_13TeV", "shape", ch.SystMap()(1.00))

        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_w_syst_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["mt","et"]).AddSyst(self.cb, "CMS_htt_norm_ff_tt_syst_13TeV", "shape", ch.SystMap()(1.00))

        self.cb.cp().process(["jetFakes"]).channel(["tt"]).AddSyst(self.cb, "CMS_htt_norm_ff_w_$CHANNEL_syst_13TeV", "shape", ch.SystMap()(1.00))
        self.cb.cp().process(["jetFakes"]).channel(["tt"]).AddSyst(self.cb, "CMS_htt_norm_ff_ttbar_$CHANNEL_syst_13TeV", "shape", ch.SystMap()(1.00))

        #jet fakes: stat norm unc
        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_ff_norm_stat_$CHANNEL_$BIN_13TeV", "lnN", ch.SystMap("channel", "bin_id")
                                                                        (["mt"], [1], 1.04)
                                                                        (["mt"], [2], 1.03)
                                                                        (["mt"], [3], 1.045)
                                                                        (["et"], [1], 1.04)
                                                                        (["et"], [2], 1.05)
                                                                        (["et"], [3], 1.065)
                                                                        (["tt"], [1], 1.03)
                                                                        (["tt"], [2], 1.04)
                                                                        (["tt"], [3], 1.05)
                                                                        )
        #jet fakes: syst norm: bin-correlated
        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_ff_norm_syst_$CHANNEL_13TeV", "lnN", ch.SystMap("channel", "bin_id")
                                                                        (["mt"], [1], 1.065)
                                                                        (["mt"], [2], 1.062)
                                                                        (["mt"], [3], 1.078)
                                                                        (["et"], [1], 1.073)
                                                                        (["et"], [2], 1.067)
                                                                        (["et"], [3], 1.083)
                                                                        (["tt"], [1], 1.026)
                                                                        (["tt"], [2], 1.032)
                                                                        (["tt"], [3], 1.040)
                                                                        )
        #jet fakes: syst norm: bin-dependent
        self.cb.cp().process(["jetFakes"]).channel(["mt","et","tt"]).AddSyst(self.cb, "CMS_htt_ff_sub_syst_$CHANNEL_$BIN_13TeV", "lnN", ch.SystMap("channel", "bin_id")
                                                                        (["mt"], [1], 1.06)
                                                                        (["mt"], [2], 1.04)
                                                                        (["mt"], [3], 1.04)
                                                                        (["et"], [1], 1.06)
                                                                        (["et"], [2], 1.04)
                                                                        (["et"], [3], 1.04)
                                                                        (["tt"], [1], 1.06)
                                                                        (["tt"], [2], 1.04)
                                    )
