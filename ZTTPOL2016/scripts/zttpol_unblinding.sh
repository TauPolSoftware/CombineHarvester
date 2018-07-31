#!/bin/sh

# Mandatory options
# $1: artus output directory
# $2: datacards output base directory
# $3: www base directory


if [ -x "$(command -v makePlots_datacardsZttPolarisation.py)" ]
then
	## ===== best choice ==============================================================================

	$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
			-i $1 -n 8 -o $2/best_choice_no_asimov --clear-output-dir --fixed-variables \
			-c em --categories em_combined_oneprong_oneprong \
			-c et --categories et_a1 et_rho et_oneprong \
			-c mt --categories mt_a1 mt_rho mt_oneprong \
			-c tt --categories tt_rho tt_combined_a1_a1 tt_combined_a1_oneprong tt_combined_oneprong_oneprong

fi

# ===== text2workspace ============================================================================

combineTool.py -M T2W -o workspace.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol -m 0 --parallel 8 \
		-i $2/best_choice_no_asimov/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt


# ===== prefit/postfit plots ======================================================================

# combine

combineTool.py -M FitDiagnostics --redefineSignalPOIs r --setParameters "pol=-0.17528,r=1" --freezeParameters pol --there -n .r_polMC -m 0 --parallel 8 \
	-d $2/best_choice_no_asimov/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root


for COMBINE_OUTPUT in $2/best_choice_no_asimov/datacards/{individual/*/*,category/*,channel/*,combined}/fitDiagnostics.r_polMC.root; do

	echo PostFitShapesFromWorkspace --postfit -m 0 -f ${COMBINE_OUTPUT}:fit_s \
		-w `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.r_polMC.root@/workspace.root@g"` \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.r_polMC.root@/ztt*_13TeV.txt@g"` \
		-o `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.r_polMC.root@/postFitShapesFromWorkspace.r_polMC.root@g"`

done | runParallel.py -n 8

# plotting

if [ -x "$(command -v makePlots_prefitPostfitPlots.py)" ]
then
	for SHAPES in $2/best_choice_no_asimov/datacards/{individual/*/*,category/*,channel/*,combined}/postFitShapesFromWorkspace.r_polMC.root; do

		echo ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -i ${SHAPES} \
			-b "\"ZTTPOSPOL ZTTNEGPOL\"" "\"ZLL ZL ZJ\"" "\"TT TTT TTJ\"" W "\"VV VVT VVJ EWKZ\"" QCD \
			-a "\" --labels ztt zll tt w vv qcd totalbkg data_obs \\\"\\\" \\\"\\\" -C ztt zll tt w vv qcd totalbkg data_obs totalbkg data_obs --x-label Discriminator --y-subplot-lims 0.5 1.5 --formats pdf png\"" \ \
			--polarisation -r --www $3/`echo ${SHAPES} | sed -e "s@${2}/@@g" -e "s@postFitShapesFromWorkspace.r_polMC.root@@g"`

done | runParallel.py -n 8
fi
