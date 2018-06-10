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

				"mt_combined_a1_oneprong" : 1060,
				"mt_combined_rho_oneprong" : 1080,
				"mt_combined_oneprong_oneprong" : 1090,

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

				"et_combined_a1_oneprong" : 1060,
				"et_combined_rho_oneprong" : 1080,
				"et_combined_oneprong_oneprong" : 1090,

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

				"em_combined_oneprong_oneprong" : 1090,
			},
			"tt" : {
				"tt_inclusive" : 1000,
				
				"tt_a1" : 1010,
				"tt_rho" : 1020,
				"tt_oneprong" : 1030,

				"tt_combined_a1_a1" : 1040,
				"tt_combined_a1_rho" : 1050,
				"tt_combined_a1_oneprong" : 1060,
				"tt_combined_rho_rho" : 1070,
				"tt_combined_rho_oneprong" : 1080,
				"tt_combined_oneprong_oneprong" : 1090,
				
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
			mt_oneprong_categories = ["mt_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_oneprong_oneprong"]]
			mt_rho_categories = ["mt_"+category for category in ["inclusive", "rho", "rho_2", "combined_rho_oneprong"]]
			mt_a1_categories = ["mt_"+category for category in ["inclusive", "a1", "a1_2", "combined_a1_oneprong"]]
			self.add_processes(
					channel="mt",
					categories=list(set(mt_oneprong_categories + mt_rho_categories + mt_a1_categories)),
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"]
			)

			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_m", "lnN", ch.SystMap("era")(["13TeV"], 1.02))

			self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap("era", "channel")(["13TeV"], ["mt", "et"], 1.045))

			self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era", "channel")(["13TeV"], ["mt", "et"], 1.02))

			# Tau ID
			self.cb.cp().channel(["mt"]).process(sig_procs).bin(mt_oneprong_categories).AddSyst(self.cb, "CMS_tauDMReco_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["mt"]).process(sig_procs).bin(mt_rho_categories).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["mt"]).process(sig_procs).bin(mt_a1_categories).AddSyst(self.cb, "CMS_tauDMReco_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))



			# extrapolation uncertainty
			self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["TTJ", "TT"], 1.10))
			self.cb.cp().channel(["mt"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["WJ", "W"], 1.2))

			# Tau ES
			self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).bin(mt_oneprong_categories).AddSyst(self.cb,"CMS_scale_t_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).bin(mt_rho_categories).AddSyst(self.cb,"CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["mt"]).process(sig_procs + all_mc_bkgs).bin(mt_a1_categories).AddSyst(self.cb,"CMS_scale_t_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))


			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA", "lnN", ch.SystMap("era", "process", "channel")(["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10))
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_mFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)(["13TeV"], ["ZLL", "ZL"], 2.00))
			self.cb.cp().channel(["mt"]).process(["ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)(["13TeV"], ["ZLL", "ZL"], 1.30))
			self.cb.cp().channel(["mt"]).process( ["ZL"]).bin(mt_oneprong_categories).AddSyst(self.cb, "CMS_mFakeTau_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["mt"]).process( ["ZL"]).bin(mt_rho_categories).AddSyst(self.cb, "CMS_mFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))

			# Top pT reweight
			#self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.0))
			
			# DY
			self.cb.cp().channel(["mt"]).process( ["ZTT","ZJ","ZL"]).AddSyst(self.cb, "CMS_htt_dyShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			
			# TTbar
			self.cb.cp().channel(["mt"]).process( ["TTJ","TTT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			
			# ZL
			self.cb.cp().channel(["mt"]).process( ["ZL"]).AddSyst(self.cb, "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			self.cb.cp().channel(["mt"]).process( ["ZL"]).AddSyst(self.cb, "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			
			# Trigger
			self.cb.cp().channel(["mt"]).process(sig_procs +  all_mc_bkgs_no_WQCD).AddSyst(self.cb, "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.02))

			# ======================================================================
			# ET channel
			et_oneprong_categories = ["et_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_oneprong_oneprong"]]
			et_rho_categories = ["et_"+category for category in ["inclusive", "rho", "rho_2", "combined_rho_oneprong"]]
			et_a1_categories = ["et_"+category for category in ["inclusive", "a1", "a1_2", "combined_a1_oneprong"]]
			self.add_processes(
					channel="et",
					categories=list(set(et_oneprong_categories + et_rho_categories + et_a1_categories)),
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"]
			)

			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_e", "lnN", ch.SystMap("era")(["13TeV"], 1.02))
			
			self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap("era", "channel")(["13TeV"], ["mt", "et"], 1.045))

			self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era", "channel")(["13TeV"], ["mt", "et"], 1.02))

			# Tau ID
			self.cb.cp().channel(["et"]).process(sig_procs).bin(et_oneprong_categories).AddSyst(self.cb, "CMS_tauDMReco_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["et"]).process(sig_procs).bin(et_rho_categories).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["et"]).process(sig_procs).bin(et_a1_categories).AddSyst(self.cb, "CMS_tauDMReco_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))



			# extrapolation uncertainty
			self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["TTJ", "TT"], 1.10))
			self.cb.cp().channel(["et"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["WJ", "W"], 1.2))

			# Tau ES
			self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).bin(et_oneprong_categories).AddSyst(self.cb,"CMS_scale_t_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).bin(et_rho_categories).AddSyst(self.cb,"CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["et"]).process(sig_procs + all_mc_bkgs).bin(et_a1_categories).AddSyst(self.cb,"CMS_scale_t_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))


			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA", "lnN", ch.SystMap("era", "process", "channel")(["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10))
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_mFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)(["13TeV"], ["ZLL", "ZL"], 2.00))
			self.cb.cp().channel(["et"]).process(["ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)(["13TeV"], ["ZLL", "ZL"], 1.30))
			self.cb.cp().channel(["et"]).process( ["ZL"]).bin(et_oneprong_categories).AddSyst(self.cb, "CMS_eFakeTau_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			self.cb.cp().channel(["et"]).process( ["ZL"]).bin(et_rho_categories).AddSyst(self.cb, "CMS_eFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))

			# Top pT reweight
			#self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.0))
			
			# DY
			self.cb.cp().channel(["et"]).process( ["ZTT","ZJ","ZL"]).AddSyst(self.cb, "CMS_htt_dyShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			
			# TTbar
			self.cb.cp().channel(["et"]).process( ["TTJ","TTT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			
			# ZL
			#self.cb.cp().channel(["et"]).process( ["ZL"]).AddSyst(self.cb, "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			#self.cb.cp().channel(["et"]).process( ["ZL"]).AddSyst(self.cb, "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
							
			# Trigger
			self.cb.cp().channel(["et"]).process(sig_procs +  all_mc_bkgs_no_WQCD).AddSyst(self.cb, "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.02))

			# ======================================================================
			# TT channel
			tt_oneprong_categories = ["tt_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_a1_oneprong", "combined_rho_oneprong", "combined_oneprong_oneprong"]]
			tt_rho_categories = ["tt_"+category for category in ["inclusive", "rho", "rho_1", "rho_2", "combined_a1_rho", "combined_rho_rho", "combined_rho_oneprong"]]
			tt_a1_categories = ["tt_"+category for category in ["inclusive", "a1", "a1_1", "a1_2", "combined_a1_a1", "combined_a1_rho", "combined_a1_oneprong"]]
			self.add_processes(
					channel="tt",
					categories=list(set(tt_oneprong_categories + tt_rho_categories + tt_a1_categories)),
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

			#self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap("era", "channel") (["13TeV"], ["mt", "et", "tt"], 1.03))

			# extrapolation uncertainty
			self.cb.cp().channel(["tt"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["TTJ", "TT"], 1.10))
			self.cb.cp().channel(["tt"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["WJ", "W"], 1.2))

			# Tau ES
			self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).bin(tt_oneprong_categories).AddSyst(self.cb,"CMS_scale_t_1prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).bin(tt_rho_categories).AddSyst(self.cb,"CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
			self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).bin(tt_a1_categories).AddSyst(self.cb,"CMS_scale_t_3prong_$ERA", "shape", ch.SystMap("era")(["13TeV"],1.00))
							

			# fake-rate
			self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA", "lnN", ch.SystMap("era", "process", "channel")(["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10))
			self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, "CMS_$ANALYSIS_mFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)(["13TeV"], ["ZLL", "ZL"], 2.00))
			self.cb.cp().channel(["tt"]).process(["ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjFakeTau_$ERA", "lnN", ch.SystMap("era", "process",)(["13TeV"], ["ZLL", "ZL"], 1.30))

			# DY
			self.cb.cp().channel(["tt"]).process( ["ZTT","ZJ","ZL"]).AddSyst(self.cb, "CMS_htt_dyShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			
			# TTBar
			self.cb.cp().channel(["tt"]).process( ["TTJ","TTT","TTJ_rest"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))

			# Top pT reweight
			#self.cb.cp().channel(["tt"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.0))

			# Trigger
			self.cb.cp().channel(["tt"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_eff_trigger_$CHANNEL_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.10))

			# ======================================================================
			# EM channel
			em_oneprong_categories = ["tt_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_oneprong_oneprong"]]
			em_rho_categories = []
			em_a1_categories = []
			self.add_processes(
					channel="em",
					categories=list(set(em_oneprong_categories + em_rho_categories + em_a1_categories)),
					bkg_processes=["ZLL", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"]
			)

			# efficiencies
			self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZLL", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_e", "lnN", ch.SystMap("era")(["13TeV"], 1.02))
			self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZLL", "TT", "VV"]).AddSyst(self.cb, "CMS_eff_m", "lnN", ch.SystMap("era")(["13TeV"], 1.02))

			# extrapolation uncertainty
			self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["TTJ", "TT"], 1.10))
			self.cb.cp().channel(["em"]).process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjExtrapol_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["WJ", "W"], 1.2))
			# b-tag
			self.cb.cp().channel(["em"]).AddSyst(self.cb, "CMS_htt_eff_b_$ERA", "lnN", ch.SystMap("channel", "process")(["em"], ["TTJ","TTT","TT"], 1.035))
			self.cb.cp().channel(["em"]).AddSyst(self.cb, "CMS_htt_eff_b_$ERA", "lnN", ch.SystMap("channel", "process")(["em"], ["TTJ","TTT","TT"], 1.05))

			self.cb.cp().channel(["em"]).AddSyst(self.cb, "CMS_htt_eff_b_$ERA", "lnN", ch.SystMap("channel", "process")(["em"], ["VV","VVT","VVJ"], 1.015))
			# e ES
			self.cb.cp().channel(["em"]).process(sig_procs + all_mc_bkgs + ["QCD"]).AddSyst(self.cb, "CMS_scale_e_$CHANNEL_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))

			# Top pT reweight
			#self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.0))

			# Trigger
			self.cb.cp().process(sig_procs + all_mc_bkgs).channel(["em"]).AddSyst(self.cb,
										 "CMS_eff_trigger_em_$ERA", "lnN", ch.SystMap("era")(["13TeV"],1.02))

			# ======================================================================
			# All channels
			#self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "ZTTPOSPOL_uniform_2", "ZTTNEGPOL_uniform_2", "lnU", ch.SystMap()(2.0))

			# lumi
			self.cb.cp().process(sig_procs + all_mc_bkgs_no_WQCD ).AddSyst(self.cb, "lumi_13TeV", "lnN", ch.SystMap("era")(["13TeV"], 1.025))

			# cross section
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZLL", "ZL", "ZJ"]).AddSyst(self.cb, "CMS_$ANALYSIS_zjXsec_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["ZLL", "ZL", "ZJ"], 1.04))
			self.cb.cp().process(["VV"]).AddSyst(self.cb, "CMS_$ANALYSIS_vvXsec_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["VV", "VVT", "VVJ"], 1.10))
			self.cb.cp().process(["TT"]).AddSyst(self.cb, "CMS_$ANALYSIS_ttjXsec_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["TTJ", "TT", "TTT", "TTJJ"], 1.06))
			self.cb.cp().process(["W"]).AddSyst(self.cb, "CMS_$ANALYSIS_wjXsec_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["WJ", "W"], 1.04))

			# signal acceptance/efficiency
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "CMS_$ANALYSIS_pdf_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["ZTT"], 1.015))
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "CMS_$ANALYSIS_QCDscale_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["ZTT"], 1.005))

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, "CMS_$ANALYSIS_qcdSyst_$ERA", "lnN", ch.SystMap("era", "process")(["13TeV"], ["QCD"], 1.10))

			# jet and met energy scale
			self.cb.cp().channel(["et","mt","tt","em"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_scale_met_clustered_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))
			self.cb.cp().channel(["et","mt","tt","em"]).process(sig_procs + all_mc_bkgs).AddSyst(self.cb, "CMS_scale_met_unclustered_$ERA", "shape", ch.SystMap("era")(["13TeV"], 1.00))

			# ======================================================================
			# Groups of systematics
			#self.cb.SetGroup("syst", [".*"])

