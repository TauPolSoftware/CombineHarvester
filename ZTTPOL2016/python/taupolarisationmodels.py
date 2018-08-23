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


class TauDecayModeMigrations(PhysicsModel):
	def __init__(self):
		self.verbose = False
		self.yields = { # [channel][reco DM][gen DM]
			"mt" : {
				0 : {
					0  : 16360.8,
					1  : 6838.47,
					2  : 1074.86,
					10 : 9.63722,
					11 : 19.6834,
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
			self.modelBuilder.doVar("gen_dm"+str(gen_decay_mode)+"[1.0,0.8,1.2]")
		
		for channel in channels:
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ZERO("@0*(1+@1*{norm})", r, gen_dm0)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(0, 1.0)) /
					      self.yields.get(channel, {}).get(  0, {}).get(0, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ONE("@0*(1-@1*{norm})", r, gen_dm1)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(1, 1.0)) /
					      self.yields.get(channel, {}).get(  0, {}).get(1, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TWO("@0*(1-@1*{norm})", r, gen_dm2)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(2, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(2, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(2, 1.0)) /
					      self.yields.get(channel, {}).get(  0, {}).get(2, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TEN("@0", r)'.format(channel=channel))
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ELEVEN("@0", r)'.format(channel=channel))
			
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ZERO("@0*(1-@1*{norm})", r, gen_dm0)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(0, 1.0)) /
					      self.yields.get(channel, {}).get(  1, {}).get(0, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ONE("@0*(1+@1*{norm})", r, gen_dm1)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(1, 1.0)) /
					      self.yields.get(channel, {}).get(  1, {}).get(1, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TWO("@0*(1+@1*{norm})", r, gen_dm2)'.format(
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
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TEN("@0*(1-@1*{norm})", r, gen_dm10)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(10, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(10, 1.0)) /
					      self.yields.get(channel, {}).get( 10, {}).get(10, 1.0))
			))
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ELEVEN("@0*(1+@1*{norm})", r, gen_dm11)'.format(
					channel=channel,
					norm=((self.yields.get(channel, {}).get( 0, {}).get(11, 1.0)+
					       self.yields.get(channel, {}).get( 1, {}).get(11, 1.0)+
					       self.yields.get(channel, {}).get(10, {}).get(11, 1.0)) /
					      self.yields.get(channel, {}).get( 10, {}).get(11, 1.0))
			))
		
		self.modelBuilder.doSet("POI", ",".join(["r"]+["gen_dm"+str(gen_dm) for gen_dm in gen_decay_modes]))

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			return bin+"_"+process
		else:
			return 1

tau_dm_migrations = TauDecayModeMigrations()

