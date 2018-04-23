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
		self.modelBuilder.doVar("pol[-0.159,-1.0,1.0]")
		self.modelBuilder.factory_('expr::pospol("@0 * (1 + @1)", r, pol)')
		self.modelBuilder.factory_('expr::negpol("@0 * (1 - @1)", r, pol)')

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

