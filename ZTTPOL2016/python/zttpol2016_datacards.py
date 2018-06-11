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

			# ======================================================================
			# MT channel
			mt_oneprong_categories = ["mt_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_oneprong_oneprong"]]
			mt_rho_categories = ["mt_"+category for category in ["inclusive", "rho", "rho_2", "combined_rho_oneprong"]]
			mt_a1_categories = ["mt_"+category for category in ["inclusive", "a1", "a1_2", "combined_a1_oneprong"]]
			self.add_processes(
					channel="mt",
					categories=list(set(mt_oneprong_categories + mt_rho_categories + mt_a1_categories)),
					bkg_processes=["ZL", "ZJ", "TTT", "TTJ", "VV", "EWKZ", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"]
			)
			
			# ======================================================================
			# ET channel
			et_oneprong_categories = ["et_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_oneprong_oneprong"]]
			et_rho_categories = ["et_"+category for category in ["inclusive", "rho", "rho_2", "combined_rho_oneprong"]]
			et_a1_categories = ["et_"+category for category in ["inclusive", "a1", "a1_2", "combined_a1_oneprong"]]
			self.add_processes(
					channel="et",
					categories=list(set(et_oneprong_categories + et_rho_categories + et_a1_categories)),
					bkg_processes=["ZL", "ZJ", "TTT", "TTJ", "VV", "EWKZ", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"]
			)
			
			# ======================================================================
			# TT channel
			tt_oneprong_categories = ["tt_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_a1_oneprong", "combined_rho_oneprong", "combined_oneprong_oneprong"]]
			tt_rho_categories = ["tt_"+category for category in ["inclusive", "rho", "rho_1", "rho_2", "combined_a1_rho", "combined_rho_rho", "combined_rho_oneprong"]]
			tt_a1_categories = ["tt_"+category for category in ["inclusive", "a1", "a1_1", "a1_2", "combined_a1_a1", "combined_a1_rho", "combined_a1_oneprong"]]
			self.add_processes(
					channel="tt",
					categories=list(set(tt_oneprong_categories + tt_rho_categories + tt_a1_categories)),
					bkg_processes=["ZL", "ZJ", "TTT", "TTJ", "VVT", "VVJ", "EWKZ", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"]
			)
			
			# ======================================================================
			# EM channel
			em_oneprong_categories = ["tt_"+category for category in ["inclusive", "oneprong", "oneprong_1", "oneprong_2", "combined_oneprong_oneprong"]]
			em_rho_categories = []
			em_a1_categories = []
			self.add_processes(
					channel="em",
					categories=list(set(em_oneprong_categories + em_rho_categories + em_a1_categories)),
					bkg_processes=["ZLL", "TT", "VV", "EWKZ", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"]
			)
			
			# ======================================================================
			# systematics
			all_mc_bkgs = ["ZL", "ZJ", "ZTTPOSPOL", "ZTTNEGPOL", "TTJ", "TTT", "TT", "W", "W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest", "VV", "VVT", "VVJ", "EWKZ"]
			all_mc_bkgs_no_W = ["ZL", "ZJ", "ZTTPOSPOL", "ZTTNEGPOL", "TTJ", "TTT", "TT", "ZJ_rest", "TTJ_rest", "VVJ_rest", "VV", "VVT", "VVJ", "EWKZ"]
			all_mc_bkgs_no_TTJ = ["ZL", "ZJ", "ZTTPOSPOL", "ZTTNEGPOL", "TTT", "TT", "ZJ_rest", "TTJ_rest", "VVJ_rest", "VV", "VVT", "VVJ", "EWKZ"]

			self.cb.cp().AddSyst(self.cb, "CMS_eff_m", "lnN", ch.SystMap("channel", "process")
					(["mt"], all_mc_bkgs_no_W, 1.02)
					(["em"], all_mc_bkgs, 1.02))

			self.cb.cp().AddSyst(self.cb, "CMS_eff_e", "lnN", ch.SystMap("channel", "process")
					(["et"], all_mc_bkgs_no_W, 1.02)
					(["em"], all_mc_bkgs, 1.02))

			# Tau Efficiency applied to all MC
			# in tautau channel the applied value depends on the number of taus which is determined by
			# gen match. WJets for example is assumed to have 1 real tau and 1 fake as is TTJ
			# compared to ZTT which has 2 real taus.
			# We also have channel specific components and fully correlated components

			# ETau & MuTau
			self.cb.cp().process(all_mc_bkgs).channel(["et", "mt"]).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap()(1.045))

			self.cb.cp().process(all_mc_bkgs).channel(["et", "mt"]).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.02))

			# TauTau - 2 real taus
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "VV", "VVT", "TTT", "EWKZ"]).channel(["tt"]).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap()(1.09))

			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "VV", "VVT", "TTT", "EWKZ"]).channel(["tt"]).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.04))

			# TauTau - 1+ jet to tau fakes
			self.cb.cp().process(["TTJ", "ZJ", "VVJ", "W", "W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest"]).channel(["tt"]).AddSyst(self.cb, "CMS_eff_t_$ERA", "lnN", ch.SystMap()(1.06))

			self.cb.cp().process(["TTJ", "ZJ", "VVJ", "W", "W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest"]).channel(["tt"]).AddSyst(self.cb, "CMS_eff_t_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.02))

			######################### Tau Id shape uncertainty (added March 08)

			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).channel(["et", "mt"]).bin(et_oneprong_categories+mt_oneprong_categories).AddSyst(self.cb, "CMS_tauDMReco_1prong_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).channel(["et", "mt"]).bin(et_rho_categories+mt_rho_categories).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).channel(["et", "mt"]).bin(et_a1_categories+mt_a1_categories).AddSyst(self.cb, "CMS_tauDMReco_3prong_$ERA", "shape", ch.SystMap()(1.00))

			###############################################################################
			# b tag and mistag rate efficiencies
			###############################################################################

			self.cb.cp().AddSyst(self.cb, "CMS_htt_eff_b_$ERA", "lnN", ch.SystMap("channel", "process")(["em"], ["TTJ", "TTT", "TT"], 1.035))

			###############################################################################
			# Electron and tau energy Scale
			###############################################################################

			self.cb.cp().process(all_mc_bkgs+["QCD"]).channel(["em"]).AddSyst(self.cb, "CMS_scale_e_$CHANNEL_$ERA", "shape", ch.SystMap()(1.00))

			# Decay Mode based TES Settings
			self.cb.cp().process(all_mc_bkgs).channel(["et", "mt", "tt"]).bin(et_oneprong_categories+mt_oneprong_categories+tt_oneprong_categories).AddSyst(self.cb, "CMS_scale_t_1prong_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process(all_mc_bkgs).channel(["et", "mt", "tt"]).bin(et_rho_categories+mt_rho_categories+tt_rho_categories).AddSyst(self.cb, "CMS_scale_t_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process(all_mc_bkgs).channel(["et", "mt", "tt"]).bin(et_a1_categories+mt_a1_categories+tt_a1_categories).AddSyst(self.cb, "CMS_scale_t_3prong_$ERA", "shape", ch.SystMap()(1.00))

			###############################################################################
			# jet and met energy Scale
			###############################################################################

			# MET Systematic shapes
			self.cb.cp().process(all_mc_bkgs).channel(["et", "mt", "tt", "em"]).AddSyst(self.cb, "CMS_scale_met_clustered_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process(all_mc_bkgs).channel(["et", "mt", "tt", "em"]).AddSyst(self.cb, "CMS_scale_met_unclustered_$ERA", "shape", ch.SystMap()(1.00))

			###############################################################################
			# Background normalization uncertainties
			###############################################################################

			# Diboson Normalisation - fully correlated
			self.cb.cp().process(["VV", "VVT", "VVJ", "VVJ_rest"]).AddSyst(self.cb, "CMS_htt_vvXsec_13TeV", "lnN", ch.SystMap()(1.05))

			# W norm, just for em, tt and the mm region where MC norm is from MC
			self.cb.cp().process(["W"]).channel(["em"]).AddSyst(self.cb, "CMS_htt_jetFakeLep_13TeV", "lnN", ch.SystMap()(1.20))

			self.cb.cp().process(["W"]).channel(["tt"]).AddSyst(self.cb, "CMS_htt_wjXsec_13TeV", "lnN", ch.SystMap()(1.04))

			# QCD norm, just for em decorrelating QCD BG for differenet categories
			self.cb.cp().process(["QCD"]).channel(["em"]).AddSyst(self.cb, "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.10))

			# QCD norm, just for tt
			self.cb.cp().process(["QCD"]).channel(["tt"]).AddSyst(self.cb, "CMS_htt_QCD_0jet_$CHANNEL_13TeV", "lnN", ch.SystMap()(1.027))

			#Iso to antiiso extrapolation
			self.cb.cp().process(["QCD"]).channel(["mt"]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.20))
			self.cb.cp().process(["QCD"]).channel(["et"]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_$CHANNEL_$ERA", "lnN", ch.SystMap()(1.20))

			#This should affect only shape (normalized to nominal values)
			self.cb.cp().process(["QCD"]).channel(["et", "mt"]).AddSyst(self.cb, "WSFUncert_$CHANNEL_0jet_$ERA", "shape", ch.SystMap()(1.00))

			# based on the Ersatz study in Run1
			self.cb.cp().process(["W"]).channel(["et", "mt"]).AddSyst(self.cb, "WHighMTtoLowMT_0jet_$ERA", "lnN", ch.SystMap()(1.10))

			###############################################################################
			# DY LO->NLO reweighting, Between no and twice the correc(on.
			###############################################################################

			self.cb.cp().process( ["ZTTPOSPOL", "ZTTNEGPOL", "ZJ", "ZL", "ZJ_rest"]).channel(["et", "mt", "tt"]).AddSyst(self.cb, "CMS_htt_dyShape_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process( ["ZTTPOSPOL", "ZTTNEGPOL", "ZL"]).channel(["em"]).AddSyst(self.cb, "CMS_htt_dyShape_$ERA", "shape", ch.SystMap()(1.00))

			###############################################################################
			# Ttbar shape reweighting, Between no and twice the correction
			###############################################################################

			self.cb.cp().process( ["TTJ", "TTT", "TTJ_rest"]).channel(["tt"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process( ["TTJ", "TTT"]).channel(["et", "mt"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process( ["TT"]).channel(["em"]).AddSyst(self.cb, "CMS_htt_ttbarShape_$ERA", "shape", ch.SystMap()(1.00))

			###############################################################################
			# ZL shape and electron/muon to tau fake only in mt and et channels (updated March 22)
			###############################################################################

			self.cb.cp().process( ["ZL"]).channel(["mt", "et"]).bin(et_oneprong_categories+mt_oneprong_categories).AddSyst(self.cb, "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process( ["ZL"]).channel(["mt", "et"]).bin(et_rho_categories+mt_rho_categories).AddSyst(self.cb, "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))

			self.cb.cp().process( ["ZL"]).channel(["mt"]).bin(mt_oneprong_categories).AddSyst(self.cb, "CMS_mFakeTau_1prong_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process( ["ZL"]).channel(["mt"]).bin(mt_rho_categories).AddSyst(self.cb, "CMS_mFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process( ["ZL"]).channel(["et"]).bin(et_oneprong_categories).AddSyst(self.cb, "CMS_eFakeTau_1prong_$ERA", "shape", ch.SystMap()(1.00))
			self.cb.cp().process( ["ZL"]).channel(["et"]).bin(et_rho_categories).AddSyst(self.cb, "CMS_eFakeTau_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))

			###############################################################################
			# jet to tau fake only in tt, mt and et channels
			###############################################################################

			self.cb.cp().process( ["TTJ", "ZJ", "VVJ", "W_rest", "ZJ_rest", "TTJ_rest", "VVJ_rest"]).channel(["tt", "mt", "et"]).AddSyst(self.cb, "CMS_htt_jetToTauFake_$ERA", "shape", ch.SystMap()(1.00))

			self.cb.cp().process( ["W"]).channel(["tt", "mt", "et"]).AddSyst(self.cb, "CMS_htt_jetToTauFake_$ERA", "shape", ch.SystMap()(1.00))

			# Recoil corrections
			# ------------------
			# These should not be applied to the W in all control regions becasuse we should
			# treat it as an uncertainty on the low/high mT factor.
			# For now we also avoid applying this to any of the high-mT control regions
			# as the exact (anti-)correlation with low mT needs to be established

			# Z->mumu CR normalization propagation
			# 0jet normalization only
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "ZJ_rest", "EWKZ"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_$CHANNEL_$ERA", "lnN", ch.SystMap("channel")(["em", "tt"], 1.07))
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "ZJ_rest", "EWKZ"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_lt_$ERA", "lnN", ch.SystMap("channel")(["et", "mt"], 1.07))

			# ======================================================================
			# Groups of systematics
			self.cb.SetGroup("syst", [".*"])

