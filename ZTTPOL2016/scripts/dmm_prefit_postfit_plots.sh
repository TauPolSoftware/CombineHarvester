#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# combine

combineTool.py -M FitDiagnostics --there -n .dmm -m 0 --parallel 8 --robustFit 1 \
	-d $1/*/datacards/combined/workspace.root \

for COMBINE_OUTPUT in $1/*/datacards/combined/fitDiagnostics.dmm.root; do

	echo PostFitShapesFromWorkspace --postfit -m 0 -f ${COMBINE_OUTPUT}:fit_s \
		-w `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm.root@/workspace.root@g"` \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm.root@/ztt*_13TeV.txt@g"` \
		-o `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm.root@/postFitShapesFromWorkspace.dmm.root@g"`

done | runParallel.py -n 8


# plotting

if [ -x "$(command -v makePlots_prefitPostfitPlots.py)" ]
then
	for SHAPES in $1/*/datacards/combined/postFitShapesFromWorkspace.dmm.root; do

		echo ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -i ${SHAPES} \
			-b ZTT_GEN_DM_ZERO ZTT_GEN_DM_ONE ZTT_GEN_DM_TWO ZTT_GEN_DM_TEN ZTT_GEN_DM_ELEVEN "\"ZLL ZL ZJ\"" "\"TT TTT TTJ\"" W "\"VV VVT VVJ EWKZ\"" QCD \
			--polarisation -r -a "\" --formats pdf png --x-label mt_m_2 --y-subplot-lims 0.5 1.5\"" \
			--www $2/`echo ${SHAPES} | sed -e "s@${1}/@@g" -e "s@postFitShapesFromWorkspace.dmm.root@@g"`

	done | runParallel.py -n 8
fi

