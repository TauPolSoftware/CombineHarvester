
# -*- coding: utf-8 -*-


class PolarisationScaleFactors(object):
	
	# initialisation with event numbers at reco level after event selection and categorisation (first two arguments)
	# and on gen level before event selection (this is rather independent of the final state or category)
	def __init__(self, n_reco_pospol, n_reco_negpol, n_gen_pospol, n_gen_negpol):
		self.n_reco_pospol = n_reco_pospol
		self.n_reco_negpol = n_reco_negpol
		self.n_gen_pospol = n_gen_pospol
		self.n_gen_negpol = n_gen_negpol
	
	# unpolarise pos. polarised sample
	def get_unpolarisation_factor_pospol(self):
		assert (self.n_gen_pospol != 0.0)
		return 1.0 / self.n_gen_pospol
	
	# unpolarise neg. polarised sample
	def get_unpolarisation_factor_negpol(self):
		assert (self.n_gen_negpol != 0.0)
		return 1.0 / self.n_gen_negpol
	
	# preserve integral at <P_tau>^gen
	def get_integral_scale_factor(self):
		numerator = 2.0 * pow(self.n_gen_pospol, 2.0) * pow(self.n_gen_negpol, 2.0) * (self.n_reco_pospol + self.n_reco_negpol)
		denominator  = self.n_reco_negpol * self.n_gen_pospol * (self.n_gen_negpol + self.n_gen_pospol * (self.n_gen_negpol - 1.0))
		denominator += self.n_reco_pospol * self.n_gen_negpol * (self.n_gen_pospol + self.n_gen_negpol * (self.n_gen_pospol - 1.0))
		assert (denominator != 0.0)
		return numerator / denominator
	
	# combined scale factor for pos. polarisation
	def get_scale_factor_pospol(self):
		return self.get_integral_scale_factor() * self.get_unpolarisation_factor_pospol()
	
	# combined scale factor for neg. polarisation
	def get_scale_factor_negpol(self):
		return self.get_integral_scale_factor() * self.get_unpolarisation_factor_negpol()
	
	# event number for pos. polarisation used as input for fit with combine
	def get_n_fit_pospol(self):
		return self.get_scale_factor_pospol() * self.n_reco_pospol
	
	# event number for neg. polarisation used as input for fit with combine
	def get_n_fit_negpol(self):
		return self.get_scale_factor_negpol() * self.n_reco_negpol

