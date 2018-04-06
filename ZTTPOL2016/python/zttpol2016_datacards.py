# -*- coding: utf-8 -*-

import logging

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.ZTTPOL2016.datacards as datacards
import CombineHarvester.ZTTPOL2016.zttpol2016_systematics as zttpol_systematics


class ZttPolarisationDatacards(datacards.Datacards):
    ''' Datacard class for the polarisation analysis. '''

    def __init__(self, cb=None):
        super(ZttPolarisationDatacards, self).__init__(cb)

        if cb is None:

            systematics = zttpol_systematics.SystematicLibary()

            # ======================================================================
            # MT channel
            self.add_processes(
                    channel="mt",
                    categories=["mt_"+category for category in ["rho", "oneprong"]], # "a1"
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
                    categories=["et_"+category for category in ["rho", "oneprong"]], # "a1"
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
                    categories=["tt_"+category for category in ["rho", "rho_1", "rho_2", "oneprong", "combined_oneprong_oneprong", "combined_rho_rho"]], # "a1"
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
