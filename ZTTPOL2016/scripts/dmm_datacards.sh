#!/bin/sh

# Mandatory options
# $1: artus output directory
# $2: datacards output base directory
# $3: www base directory


# ===== input templates + datacards ===============================================================

if [ -x "$(command -v makePlots_datacardsZttPolarisation.py)" ]
then

#	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
#			-i $1 -n 8 -o $2/asimov_m_2 --clear-output-dir -x m_2 --decay-mode-migrations \
#			-c et --categories et_a1 et_rho et_oneprong \
#			-c mt --categories mt_a1 mt_rho mt_oneprong \
#			--use-asimov-dataset

	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/data_m_2 --clear-output-dir -x m_2 --decay-mode-migrations \
			-c et --categories et_a1 et_rho et_oneprong \
			-c mt --categories mt_a1 mt_rho mt_oneprong

fi


# ===== text2workspace ============================================================================

combineTool.py -M T2W -o workspace_gen_mixing.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:tau_dm_migrations_gen_mixing -m 0 --parallel 8 \
		-i $2/*/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt

combineTool.py -M T2W -o workspace_reco_mixing.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:tau_dm_migrations_reco_mixing -m 0 --parallel 8 \
		-i $2/*/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt


# ===== plots =====================================================================================

if [ -x "$(command -v makePlots_prefitPostfitPlots.py)" ]
then

	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -n 8 \
			-i $2/*/datacards/common/ztt.input_13TeV.root \
			-b ZTT_GEN_DM_ZERO ZTT_GEN_DM_ONE ZTT_GEN_DM_TWO ZTT_GEN_DM_TEN ZTT_GEN_DM_ELEVEN "ZLL ZL ZJ" "TT TTT TTJ" W "VV VVT VVJ EWKZ" QCD \
			--polarisation -r -a " --formats pdf png --x-label mt_m_2 --y-subplot-lims 0.5 1.5" --www $3/inputs

fi


if [ -x "$(command -v makePlots_shapeUncertainties.py)" ]
then
	${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_shapeUncertainties.py \
			$2/*/datacards/common/ztt.*.root -r --www $3/shape_uncertainties -n 8 -a " --formats pdf png --x-label mt_m_2 --y-subplot-lims 0.5 1.5"
fi

