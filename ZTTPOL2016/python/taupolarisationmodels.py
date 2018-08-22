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
					0  : 1.0,
					1  : 1.0,
					2  : 1.0,
					10 : 1.0,
					11 : 1.0,
				},
				1 : {
					0  : 1.0,
					1  : 1.0,
					2  : 1.0,
					10 : 1.0,
					11 : 1.0,
				},
				10 : {
					0  : 1.0,
					1  : 1.0,
					2  : 1.0,
					10 : 1.0,
					11 : 1.0,
				},
			},
			"et" : {
				0 : {
					0  : 1.0,
					1  : 1.0,
					2  : 1.0,
					10 : 1.0,
					11 : 1.0,
				},
				1 : {
					0  : 1.0,
					1  : 1.0,
					2  : 1.0,
					10 : 1.0,
					11 : 1.0,
				},
				10 : {
					0  : 1.0,
					1  : 1.0,
					2  : 1.0,
					10 : 1.0,
					11 : 1.0,
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
		
		for gen_decay_mode in gen_decay_modes:
			self.modelBuilder.doVar("gen_dm"+str(gen_decay_mode)+"[1.0,0.0,2.0]")
		
		for channel in channels:
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ZERO("1+@0/{integral}", gen_dm0)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(0, 1.0))
			)
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ONE("1-@0/{integral}", gen_dm1)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(1, 1.0))
			)
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TWO("1-@0/{integral}", gen_dm2)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(2, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(2, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(2, 1.0))
			)
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_TEN("1")')
			self.modelBuilder.factory_('expr::{channel}_oneprong_ZTT_GEN_DM_ELEVEN("1")')
			
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ZERO("1-@0/{integral}", gen_dm0)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(0, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(0, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(0, 1.0))
			)
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ONE("1+@0/{integral}", gen_dm1)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(1, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(1, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(1, 1.0))
			)
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TWO("1+@0/{integral}", gen_dm2)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(2, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(2, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(2, 1.0))
			)
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_TEN("1")')
			self.modelBuilder.factory_('expr::{channel}_rho_ZTT_GEN_DM_ELEVEN("1")')
			
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ZERO("1")')
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ONE("1")')
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TWO("1")')
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_TEN("1-@0/{integral}", gen_dm10)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(10, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(10, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(10, 1.0))
			)
			self.modelBuilder.factory_('expr::{channel}_a1_ZTT_GEN_DM_ELEVEN("1+@0/{integral}", gen_dm11)'.format(
					channel=channel,
					integral=(self.yields.get(channel, {}).get( 0, {}).get(11, 1.0)+
					          self.yields.get(channel, {}).get( 1, {}).get(11, 1.0)+
					          self.yields.get(channel, {}).get(10, {}).get(11, 1.0))
			)
		
		self.modelBuilder.doSet("POI", ",".join(["gen_dm"+str(gen_dm) for gen_dm in gen_decay_modes]))

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			return bin+"_"+process
		else:
			return 1

tau_dm_migrations = TauDecayModeMigrations()

