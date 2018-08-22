#!/bin/sh

# Mandatory options
# $1: artus output directory
# $2: datacards output base directory


if [ -x "$(command -v makePlots_datacardsZttPolarisation.py)" ]
then

	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/dmm_m_2 --clear-output-dir --use-asimov-dataset -x m_2 --decay-mode-migrations \
			-c et --categories et_a1 et_rho et_oneprong \
			-c mt --categories mt_a1 mt_rho mt_oneprong

fi

# ===== text2workspace ============================================================================

combineTool.py -M T2W -o workspace.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol -m 0 --parallel 8 \
		-i $2/*/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt

