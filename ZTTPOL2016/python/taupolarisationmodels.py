from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

import ROOT

import array
import os


class ZttPolarisation(PhysicsModel):
	def __init__(self):
		self.verbose = False

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
		self.modelBuilder.doVar("r[1.0,0.0,5.0]")
		self.modelBuilder.doVar("pol[-0.17528,-1.0,1.0]") # http://pdglive.lbl.gov/DataBlock.action?node=S044AT
		self.modelBuilder.factory_('expr::pospol("@0 * (1 + @1) / 2.0", r, pol)')
		self.modelBuilder.factory_('expr::negpol("@0 * (1 - @1) / 2.0", r, pol)')

		self.modelBuilder.doSet("POI","r,pol")

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			if "pospol" in process.lower():
				return "pospol"
			elif "negpol" in process.lower():
				return "negpol"
			else:
				return "r"
		else:
			return 1

ztt_pol = ZttPolarisation()


class ZttWeakMixingAngle(PhysicsModel):
	def __init__(self):
		self.verbose = False

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True
		self.categories = ["mt_oneprong", "mt_rho", "mt_a1",
		                   "et_oneprong", "et_rho", "et_a1",
		                   "tt_combined_oneprong_oneprong", "tt_rho", "tt_combined_a1_oneprong", "tt_combined_a1_a1",
		                   "em_combined_oneprong_oneprong"]

	def getPolarisationVsWeakMixingAngleValues(self):
		root_file = ROOT.TFile.Open(os.path.expandvars("$CMSSW_BASE/src/TauPolSoftware/CalibrationCurve/data/calibration_curves.root"), "READ")
		values = {}
		
		for category in self.categories:
			
			graph = root_file.Get(os.path.join(category, "combined_uncs/pol_vs_sin2theta"))
			n_points = graph.GetN()
			x_values = graph.GetX()
			x_values = array.array("d", [x_values[index] for index in xrange(n_points)])
			y_values = graph.GetY()
			y_values = array.array("d", [y_values[index] for index in xrange(n_points)])
			values[category] = (x_values, y_values)
		
		root_file.Close()
		return values
			
	
	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
		self.modelBuilder.doVar("r[1.0,0.0,5.0]")
		self.modelBuilder.doVar("sintwotheta[0.2208,0.15,0.3]")
		sintwotheta = self.modelBuilder.out.var("sintwotheta")
		
		spline_values = self.getPolarisationVsWeakMixingAngleValues()
		for category in self.categories:
			x_values, y_values = spline_values[category]
			spline = ROOT.RooSpline1D("pol_"+category, "pol_"+category, sintwotheta, len(x_values), x_values, y_values, "CSPLINE")
			self.modelBuilder.out._import(spline)
			self.modelBuilder.factory_('expr::pospol_{category}("@0 * (1 + @1) / 2.0", r, pol_{category})'.format(category=category))
			self.modelBuilder.factory_('expr::negpol_{category}("@0 * (1 - @1) / 2.0", r, pol_{category})'.format(category=category))

		self.modelBuilder.doSet("POI","r,sintwotheta")

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			if "pospol" in process.lower():
				return "pospol_"+bin
			elif "negpol" in process.lower():
				return "negpol_"+bin
			else:
				return "r"
		else:
			return 1

ztt_weak_mixing_angle = ZttWeakMixingAngle()


class TauDecayModeMigrationsGenMixing(PhysicsModel):
	def __init__(self):
		self.verbose = False
		self.yields = { # [channel][reco DM][gen DM]
			"mt" : {
				0 : {
					0  : 16914.2,
					1  : 7049.33,
					2  : 1108.69,
					10 : 9.63722,
					11 : 20.6968,
				},
				1 : {
					0  : 2728.48,
					1  : 37211.8,
					2  : 19139.3,
					10 : 28.0366,
					11 : 75.6974,
				},
				10 : {
					0  : 120.157,
					1  : 328.659,
					2  : 135.359,
					10 : 27649.1,
					11 : 5436.2,
				},
			},
			"et" : {
				0 : {
					0  : 3533.01,
					1  : 1171.72,
					2  : 135.547,
					10 : 2.66985,
					11 : 8.81842,
				},
				1 : {
					0  : 525.47,
					1  : 9308.79,
					2  : 5042.23,
					10 : 3.71993,
					11 : 16.9075,
				},
				10 : {
					0  : 29.6033,
					1  : 57.2881,
					2  : 16.3246,
					10 : 7918.84,
					11 : 1477.22,
				},
			},
		}

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
		
		channels = ["mt", "et"]
		gen_decay_modes = [0, 1, 2]#, 10, 11]
		
		channel = "mt"
		self.modelBuilder.doVar("r[1.0,0.5,1.5]")
		self.modelBuilder.doVar("x0[0.0,{norm_plus},{norm_minus}]".format(
				norm_plus =(self.yields.get(channel, {}).get(  0, {}).get(0, 1.0) * (-1) /
					        (self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					         self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(0, 1.0))),
				norm_minus=(self.yields.get(channel, {}).get(  1, {}).get(0, 1.0) /
					        (self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					         self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(0, 1.0)))
		))
		self.modelBuilder.doVar("x1[0.0,{norm_plus},{norm_minus}]".format(
				norm_plus =(self.yields.get(channel, {}).get(  1, {}).get(1, 1.0) * (-1) /
					        (self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					         self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(1, 1.0))),
				norm_minus=(self.yields.get(channel, {}).get(  0, {}).get(1, 1.0) /
					        (self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					         self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(1, 1.0)))
		))
		self.modelBuilder.doVar("x2[0.0,{norm_plus},{norm_minus}]".format(
				norm_plus =(self.yields.get(channel, {}).get(  1, {}).get(2, 1.0) * (-1) /
					        (self.yields.get(channel, {}).get( 0, {}).get(2, 1.0)+
					         self.yields.get(channel, {}).get( 1, {}).get(2, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(2, 1.0))),
				norm_minus=(self.yields.get(channel, {}).get(  0, {}).get(2, 1.0) /
					        (self.yields.get(channel, {}).get( 0, {}).get(2, 1.0)+
					         self.yields.get(channel, {}).get( 1, {}).get(2, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(2, 1.0)))
		))
#		for gen_decay_mode in gen_decay_modes:
#			self.modelBuilder.doVar("x"+str(gen_decay_mode)+"[0.0,-1.0,1.0]")
		
		for channel in channels:
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ZERO("@0*(1+@1*{norm})", r, x0)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(0, 1.0)) /
					      self.yields.get(channel, {}).get(  0, {}).get(0, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ONE("@0*(1-@1*{norm})", r, x1)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(1, 1.0)) /
					      self.yields.get(channel, {}).get(  0, {}).get(1, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TWO("@0*(1-@1*{norm})", r, x2)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(2, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(2, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(2, 1.0)) /
					      self.yields.get(channel, {}).get(  0, {}).get(2, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TEN("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ELEVEN("@0", r)'.format(channel=channel))
			
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ZERO("@0*(1-@1*{norm})", r, x0)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(0, 1.0)) /
					      self.yields.get(channel, {}).get(  1, {}).get(0, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ONE("@0*(1+@1*{norm})", r, x1)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(1, 1.0)) /
					      self.yields.get(channel, {}).get(  1, {}).get(1, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TWO("@0*(1+@1*{norm})", r, x2)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(2, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(2, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(2, 1.0)) /
					      self.yields.get(channel, {}).get(  1, {}).get(2, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TEN("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ELEVEN("@0", r)'.format(channel=channel))
			
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ZERO("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ONE("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TWO("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TEN("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ELEVEN("@0", r)'.format(channel=channel))
		
		self.modelBuilder.doSet("POI", ",".join(["r"]+["x"+str(gen_decay_mode) for gen_decay_mode in gen_decay_modes]))

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			return bin+"_"+process
		else:
			return 1

tau_dm_migrations_gen_mixing = TauDecayModeMigrationsGenMixing()


class TauDecayModeMigrationsRecoMixing(PhysicsModel):
	def __init__(self):
		self.verbose = False
		self.yields = { # [channel][reco DM][gen DM]
			"mt" : {
				0 : {
					0  : 16914.2,
					1  : 7049.33,
					2  : 1108.69,
					10 : 9.63722,
					11 : 20.6968,
				},
				1 : {
					0  : 2728.48,
					1  : 37211.8,
					2  : 19139.3,
					10 : 28.0366,
					11 : 75.6974,
				},
				10 : {
					0  : 120.157,
					1  : 328.659,
					2  : 135.359,
					10 : 27649.1,
					11 : 5436.2,
				},
			},
			"et" : {
				0 : {
					0  : 3533.01,
					1  : 1171.72,
					2  : 135.547,
					10 : 2.66985,
					11 : 8.81842,
				},
				1 : {
					0  : 525.47,
					1  : 9308.79,
					2  : 5042.23,
					10 : 3.71993,
					11 : 16.9075,
				},
				10 : {
					0  : 29.6033,
					1  : 57.2881,
					2  : 16.3246,
					10 : 7918.84,
					11 : 1477.22,
				},
			},
		}

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
		
		channels = ["mt", "et"]
		gen_decay_modes = [0, 1, 2, 10, 11]
		reco_decay_modes = [0, 1, 10]
		
		channel = "mt"
		self.modelBuilder.doVar("r[1.0,0.5,1.5]")
		self.modelBuilder.doVar("x0[0.0,{norm_plus},{norm_minus}]".format(
				norm_plus =(self.yields.get(channel, {}).get( 0, {}).get( 0, 1.0) * (-1) /
					        (self.yields.get(channel, {}).get(0, {}).get( 0, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get( 1, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get( 2, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get(10, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get(11, 1.0))),
				norm_minus=(self.yields.get(channel, {}).get( 0, {}).get( 1, 1.0) /
					        (self.yields.get(channel, {}).get(0, {}).get( 0, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get( 1, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get( 2, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get(10, 1.0)+
					         self.yields.get(channel, {}).get(0, {}).get(11, 1.0)))
		))
		self.modelBuilder.doVar("x1[0.0,{norm_plus},{norm_minus}]".format(
				norm_plus =(self.yields.get(channel, {}).get( 1, {}).get( 1, 1.0) * (-1) /
					        (self.yields.get(channel, {}).get(1, {}).get( 0, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get( 1, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get( 2, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get(10, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get(11, 1.0))),
				norm_minus=(self.yields.get(channel, {}).get( 1, {}).get( 2, 1.0) /
					        (self.yields.get(channel, {}).get(1, {}).get( 0, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get( 1, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get( 2, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get(10, 1.0)+
					         self.yields.get(channel, {}).get(1, {}).get(11, 1.0)))
		))
		self.modelBuilder.doVar("x10[0.0,{norm_plus},{norm_minus}]".format(
				norm_plus =(self.yields.get(channel, {}).get( 10, {}).get(10, 1.0) * (-1) /
					        (self.yields.get(channel, {}).get(10, {}).get( 0, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get( 1, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get( 2, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(10, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(11, 1.0))),
				norm_minus=(self.yields.get(channel, {}).get( 10, {}).get(11, 1.0) /
					        (self.yields.get(channel, {}).get(10, {}).get( 0, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get( 1, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get( 2, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(10, 1.0)+
					         self.yields.get(channel, {}).get(10, {}).get(11, 1.0)))
		))
#		for reco_decay_mode in reco_decay_modes:
#			self.modelBuilder.doVar("x"+str(reco_decay_mode)+"[0.0,-1.0,1.0]")
		
		for channel in channels:
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ZERO("@0*(1+@1*{norm})", r, x0)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get(0, {}).get( 0, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get( 1, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get( 2, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 0, {}).get( 0, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ONE("@0*(1-@1*{norm})", r, x0)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get(0, {}).get( 0, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get( 1, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get( 2, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(0, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 0, {}).get( 1, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TWO("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TEN("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ELEVEN("@0", r)'.format(channel=channel))
			
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ZERO("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ONE("@0*(1+@1*{norm})", r, x1)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get(1, {}).get( 0, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get( 1, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get( 2, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 1, {}).get( 1, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TWO("@0*(1-@1*{norm})", r, x1)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get(1, {}).get( 0, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get( 1, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get( 2, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(1, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 1, {}).get( 2, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TEN("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ELEVEN("@0", r)'.format(channel=channel))
			
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ZERO("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ONE("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TWO("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TEN("@0*(1+@1*{norm})", r, x10)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get(10, {}).get( 0, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get( 1, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get( 2, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 10, {}).get(10, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ELEVEN("@0*(1-@1*{norm})", r, x10)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get(10, {}).get( 0, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get( 1, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get( 2, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 10, {}).get(11, 1.0))
			))
		
		self.modelBuilder.doSet("POI", ",".join(["r"]+["x"+str(reco_decay_mode) for reco_decay_mode in reco_decay_modes]))

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			return bin+"_"+process
		else:
			return 1

tau_dm_migrations_reco_mixing = TauDecayModeMigrationsRecoMixing()


class TauDecayModeMigrationsMatrix(PhysicsModel):
	def __init__(self):
		self.verbose = False

	def setPhysicsOptions(self, physOptions):
		for po in physOptions:
			if po.startswith("verbose"):
				self.verbose = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
		
		self.modelBuilder.doVar("r[1.0,0.0,2.0]")
		migrations = [
			"genZero_recoZero",
			"genOne_recoZero",
			"genTwo_recoZero",
			"genTen_recoZero",
			"genEleven_recoZero",
			
			"genZero_recoOne",
			"genOne_recoOne",
			"genTwo_recoOne",
			"genTen_recoOne",
			"genEleven_recoOne",
			
			"genZero_recoTen",
			"genOne_recoTen",
			"genTwo_recoTen",
			"genTen_recoTen",
			"genEleven_recoTen",
		]
		for migration in migrations:
			self.modelBuilder.doVar(migration+"[1.0,0.0,2.0]")
		
		channels = ["mt", "et"]
		for channel in channels:
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ZERO("@0*@1", r, genZero_recoZero)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ONE("@0*@1", r, genOne_recoZero)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TWO("@0*@1", r, genTwo_recoZero)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TEN("@0*@1", r, genTen_recoZero)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ELEVEN("@0*@1", r, genEleven_recoZero)'.format(channel=channel))
			
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ZERO("@0*@1", r, genZero_recoOne)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ONE("@0*@1", r, genOne_recoOne)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TWO("@0*@1", r, genTwo_recoOne)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TEN("@0*@1", r, genTen_recoOne)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ELEVEN("@0*@1", r, genEleven_recoOne)'.format(channel=channel))
			
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ZERO("@0*@1", r, genZero_recoTen)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ONE("@0*@1", r, genOne_recoTen)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TWO("@0*@1", r, genTwo_recoTen)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TEN("@0*@1", r, genTen_recoTen)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ELEVEN("@0*@1", r, genEleven_recoTen)'.format(channel=channel))
		
		self.modelBuilder.doSet("POI", ",".join(["r"]+migrations))

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			return bin+"_"+process
		else:
			return 1

tau_dm_migrations_matrix = TauDecayModeMigrationsMatrix()

