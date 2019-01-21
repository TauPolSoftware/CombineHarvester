from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

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
		self.modelBuilder.doVar("pol[-0.143,-1.0,1.0]") # http://pdglive.lbl.gov/DataBlock.action?node=S044AT
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
		gen_decay_modes = [0, 1, 2, 10, 11]
		reco_decay_modes = [0, 1, 10]
		
		self.modelBuilder.doVar("r[1.0,0.5,1.5]")
		for gen_decay_mode in gen_decay_modes:
			self.modelBuilder.doVar("x"+str(gen_decay_mode)+"[0.0,-1.0,1.0]")
#		self.modelBuilder.doVar("r[0.9,0.6,1.5]")
#		self.modelBuilder.doVar("x0[0.06,-0.04,0.18]")
#		self.modelBuilder.doVar("x1[0.0,-0.1,0.1]")
#		self.modelBuilder.doVar("x2[0.02,-0.2,0.25]")
#		self.modelBuilder.doVar("x10[0.14,0.04,0.22]")
#		self.modelBuilder.doVar("x11[0.85,0.5,1.0]")
		
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
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TEN("@0*(1+@1*{norm})", r, x10)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(10, 1.0)) /
					      self.yields.get(channel, {}).get( 10, {}).get(10, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ELEVEN("@0*(1-@1*{norm})", r, x11)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(11, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(11, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 10, {}).get(11, 1.0))
			))
		
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
					         self.yields.get(channel, {}).get(0, {}).get(11, 1.0))),
		
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
					         self.yields.get(channel, {}).get(1, {}).get(11, 1.0))),
		
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
					         self.yields.get(channel, {}).get(10, {}).get(11, 1.0))),
		
		))
#		for reco_decay_mode in reco_decay_modes:
#			self.modelBuilder.doVar("x"+str(reco_decay_mode)+"[0.0,-1.0,1.0]")
#		self.modelBuilder.doVar("r[0.95,0.6,1.5]")
#		self.modelBuilder.doVar("x0[0.1,-0.5,0.6]")
#		self.modelBuilder.doVar("x1[-0.01,-0.1,0.08]")
#		self.modelBuilder.doVar("x10[0.12,0.02,0.22]")
		
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

