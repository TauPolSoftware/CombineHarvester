
# -*- coding: utf-8 -*-

import math
import numbers

# the calculations here use the uncertainties package for the error propagation
# use <return value>.nominal_value to retrive the central value
# http://uncertainties-python-package.readthedocs.io/en/latest/user_guide.html
import CombineHarvester.ZTTPOL2016.uncertainties.uncertainties as uncertainties


class PolarisationScaleFactors(object):
	
	# initialisation with event numbers at reco level after event selection and categorisation (first two arguments)
	# and on gen level before event selection (this is rather independent of the final state or category)
	def __init__(self, n_reco_pospol, n_reco_negpol, n_gen_pospol, n_gen_negpol):
		print type(n_reco_pospol)
		self.n_reco_pospol = uncertainties.ufloat(n_reco_pospol, math.sqrt(n_reco_pospol)) if type(n_reco_pospol) == numbers.Number else n_reco_pospol
		self.n_reco_negpol = uncertainties.ufloat(n_reco_negpol, math.sqrt(n_reco_negpol)) if type(n_reco_negpol) == numbers.Number else n_reco_negpol
		self.n_gen_pospol = uncertainties.ufloat(n_gen_pospol, math.sqrt(n_gen_pospol)) if type(n_gen_pospol) == numbers.Number else n_gen_pospol
		self.n_gen_negpol = uncertainties.ufloat(n_gen_negpol, math.sqrt(n_gen_negpol)) if type(n_gen_negpol) == numbers.Number else n_gen_negpol
	
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

