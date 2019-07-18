#!/bin/sh

# Mandatory options
# $1: artus output directory
# $2: datacards output base directory


if [ -x "$(command -v makePlots_datacardsZttPolarisation.py)" ]
then

	## ===== best choice ===============================================================================

	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/best_choice --clear-output-dir --use-asimov-dataset --fixed-variables best_choice \
			-c em --categories em_combined_oneprong_oneprong \
			-c et --categories et_a1 et_rho et_oneprong \
			-c mt --categories mt_rho mt_a1 mt_oneprong \
			-c tt --categories tt_rho tt_combined_a1_a1 tt_combined_a1_oneprong tt_combined_oneprong_oneprong #\
#			--modify-unpolarisation-value -0.2208


	## ===== best choice (no SVfit) ====================================================================

	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/best_choice_no_svfit --clear-output-dir --use-asimov-dataset --fixed-variables best_choice_no_svfit \
			-c em --categories em_combined_oneprong_oneprong \
			-c et --categories et_a1 et_rho et_oneprong \
			-c mt --categories mt_a1 mt_rho mt_oneprong \
			-c tt --categories tt_rho tt_combined_a1_a1 tt_combined_a1_oneprong tt_combined_oneprong_oneprong #\
#			--modify-unpolarisation-value -0.2208


	## ===== omegaBarSvfit =============================================================================

	# polarisationOmegaBarSvfit_1 (em, et, mt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/omegaBarSvfitM91_1 --clear-output-dir --use-asimov-dataset \
			-c em --categories em_oneprong_1 \
			-c et --categories et_oneprong_1 \
			-c mt --categories mt_oneprong_1 #\
#			--modify-unpolarisation-value -0.2208

	# polarisationOmegaBarSvfit_2 (em, et, mt), polarisationOmegaBarSvfit_1/2 (tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/omegaBarSvfitM91_2 --clear-output-dir --use-asimov-dataset \
			-c em --categories em_oneprong_2 \
			-c et --categories et_a1 et_rho et_oneprong \
			-c mt --categories mt_a1 mt_rho mt_oneprong \
			-c tt --categories tt_a1 tt_rho tt_oneprong #\
#			--modify-unpolarisation-value -0.2208

	# polarisationCombinedOmegaBarSvfit (em, et, mt, tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/combinedOmegaBarSvfitM91 --clear-output-dir --use-asimov-dataset \
			-c em --categories em_combined_oneprong_oneprong \
			-c et --categories et_combined_a1_oneprong et_combined_rho_oneprong et_combined_oneprong_oneprong \
			-c mt --categories mt_combined_a1_oneprong mt_combined_rho_oneprong mt_combined_oneprong_oneprong \
			-c tt --categories tt_combined_a1_a1 tt_combined_a1_rho tt_combined_a1_oneprong tt_combined_rho_rho tt_combined_rho_oneprong tt_combined_oneprong_oneprong #\
#			--modify-unpolarisation-value -0.2208


	## ===== omegaBarSvfitM91 ==========================================================================

	# polarisationOmegaBarSvfitM91_1 (em, et, mt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/omegaBarSvfit_1 --clear-output-dir --use-asimov-dataset --omega-version BarSvfitM91 \
			-c em --categories em_oneprong_1 \
			-c et --categories et_oneprong_1 \
			-c mt --categories mt_oneprong_1 #\
#			--modify-unpolarisation-value -0.2208

	# polarisationOmegaBarSvfitM91_2 (em, et, mt), polarisationOmegaBarSvfit_1/2 (tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/omegaBarSvfit_2 --clear-output-dir --use-asimov-dataset --omega-version BarSvfitM91 \
			-c em --categories em_oneprong_2 \
			-c et --categories et_a1 et_rho et_oneprong \
			-c mt --categories mt_a1 mt_rho mt_oneprong \
			-c tt --categories tt_a1 tt_rho tt_oneprong #\
#			--modify-unpolarisation-value -0.2208

	# combinedOmegaBarSvfit (em, et, mt, tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/combinedOmegaBarSvfit --clear-output-dir --use-asimov-dataset --omega-version BarSvfitM91 \
			-c em --categories em_combined_oneprong_oneprong \
			-c et --categories et_combined_a1_oneprong et_combined_rho_oneprong et_combined_oneprong_oneprong \
			-c mt --categories mt_combined_a1_oneprong mt_combined_rho_oneprong mt_combined_oneprong_oneprong \
			-c tt --categories tt_combined_a1_a1 tt_combined_a1_rho tt_combined_a1_oneprong tt_combined_rho_rho tt_combined_rho_oneprong tt_combined_oneprong_oneprong #\
#			--modify-unpolarisation-value -0.2208


	## ===== omegaVisible(Svfit) =======================================================================

	# polarisationOmegaVisibleSvfit_1 (et, mt), polarisationOmegaBarSvfit_1/2 (tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/omegaVisible_2 --clear-output-dir --use-asimov-dataset --omega-version VisibleSvfit \
			-c et --categories et_rho \
			-c mt --categories mt_rho \
			-c tt --categories tt_rho #\
#			--modify-unpolarisation-value -0.2208

	# polarisationCombinedOmegaVisibleSvfit (tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/combinedOmegaVisible --clear-output-dir --use-asimov-dataset --omega-version VisibleSvfit \
			-c tt --categories tt_combined_rho_rho #\
#			--modify-unpolarisation-value -0.2208


	## ===== visible mass ==============================================================================

	# m_vis, inclusive (em, et, mt, tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/m_vis_inclusive --clear-output-dir --use-asimov-dataset -x m_vis \
			-c em --categories em_oneprong_1 \
			-c et --categories et_oneprong_1 \
			-c mt --categories mt_oneprong_1 \
			-c tt --categories tt_inclusive \
#			--modify-unpolarisation-value -0.2208

	# m_vis, omega categorisation (tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/m_vis_omegaCategories --clear-output-dir --use-asimov-dataset -x m_vis \
			-c tt --categories tt_a1 tt_rho tt_oneprong #\
#			--modify-unpolarisation-value -0.2208

	# m_vis, combinedOmega categorisation (em, et, mt, tt)
	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/m_vis_combinedOmegaCategories --clear-output-dir --use-asimov-dataset -x m_vis \
			-c em --categories em_combined_oneprong_oneprong \
			-c et --categories et_combined_a1_oneprong et_combined_rho_oneprong et_combined_oneprong_oneprong \
			-c mt --categories mt_combined_a1_oneprong mt_combined_rho_oneprong mt_combined_oneprong_oneprong \
			-c tt --categories tt_combined_a1_a1 tt_combined_a1_rho tt_combined_a1_oneprong tt_combined_rho_rho tt_combined_rho_oneprong tt_combined_oneprong_oneprong #\
#			--modify-unpolarisation-value -0.2208

fi

# ===== text2workspace ============================================================================

combineTool.py -M T2W -o workspace.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol -m 0 --parallel 8 \
		-i $2/*/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt

