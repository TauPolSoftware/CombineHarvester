#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# combine

# fits to provide starting plots for diagnostics
combineTool.py -M MultiDimFit --algo singles \
	--saveWorkspace -n .dmm_reco_mixing --saveFitResult \
	-d $1/*reco*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace_reco_mixing.root \
	--setParameters r=1 --freezeParameters r --redefineSignalPOIs x0,x1,x10 \
	--there -m 0 --parallel 1 \
	--robustFit 1

combineTool.py -M MultiDimFit --algo singles \
	--saveWorkspace -n .dmm_gen_mixing --saveFitResult \
	-d $1/*gen*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace_gen_mixing.root \
	--setParameters r=1 --freezeParameters r --redefineSignalPOIs x0,x1,x2 \
	--there -m 0 --parallel 1 \
	--robustFit 1


# fit diagnostics
#combineTool.py -M FitDiagnostics --there -n .dmm_gen_mixing -m 0 --parallel 8 --robustFit 1 \
#	--setParameters r=1 --freezeParameters r \
#	-d $1/*/datacards/{channel/*,combined}/workspace_gen_mixing.root

combineTool.py -M FitDiagnostics --there -n .dmm_reco_mixing -m 0 --parallel 8 --robustFit 1 \
	-d $1/*reco*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace_reco_mixing.root \
	--setParameters r=1 --freezeParameters r --redefineSignalPOIs x0,x1,x10 \
	--customStartingPoint --skipBOnlyFit

combineTool.py -M FitDiagnostics --there -n .dmm_gen_mixing -m 0 --parallel 8 --robustFit 1 \
	-d $1/*gen*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace_gen_mixing.root \
	--setParameters r=1 --freezeParameters r --redefineSignalPOIs x0,x1,x2 \
	--customStartingPoint --skipBOnlyFit


combineTool.py -M FitDiagnostics --there -n .dmm_reco_mixing -m 0 --parallel 8 --robustFit 1 \
	-d $1/*reco*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.dmm_reco_mixing.MultiDimFit.mH0.root --snapshotName MultiDimFit -w w \
	--setParameters r=1 --freezeParameters r --redefineSignalPOIs x0,x1,x10 \
	--customStartingPoint --skipBOnlyFit

combineTool.py -M FitDiagnostics --there -n .dmm_gen_mixing -m 0 --parallel 8 --robustFit 1 \
	-d $1/*gen*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.dmm_gen_mixing.MultiDimFit.mH0.root --snapshotName MultiDimFit -w w \
	--setParameters r=1 --freezeParameters r --redefineSignalPOIs x0,x1,x2 \
	--customStartingPoint --skipBOnlyFit

#for COMBINE_OUTPUT in `ls $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/fitDiagnostics.dmm_gen_mixing.root 2> /dev/null`; do

#	echo PostFitShapesFromWorkspace --postfit -m 0 -f ${COMBINE_OUTPUT}:fit_s \
#		-w `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_gen_mixing.root@/workspace_gen_mixing.root@g"` \
#		-d `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_gen_mixing.root@/ztt*_13TeV.txt@g"` \
#		-o `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_gen_mixing.root@/postFitShapesFromWorkspace.dmm_gen_mixing.root@g"`

#done | runParallel.py -n 8

for COMBINE_OUTPUT in `ls $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/fitDiagnostics.dmm_reco_mixing.root 2> /dev/null`; do

	echo PostFitShapesFromWorkspace --postfit -m 0 -f ${COMBINE_OUTPUT}:fit_s \
		-w `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_reco_mixing.root@/workspace_reco_mixing.root@g"` \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_reco_mixing.root@/ztt*_13TeV.txt@g"` \
		-o `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_reco_mixing.root@/postFitShapesFromWorkspace.dmm_reco_mixing.root@g"`

done | runParallel.py -n 8

for COMBINE_OUTPUT in `ls $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/fitDiagnostics.dmm_gen_mixing.root 2> /dev/null`; do

	echo PostFitShapesFromWorkspace --postfit -m 0 -f ${COMBINE_OUTPUT}:fit_s \
		-w `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_gen_mixing.root@/workspace_gen_mixing.root@g"` \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_gen_mixing.root@/ztt*_13TeV.txt@g"` \
		-o `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.dmm_gen_mixing.root@/postFitShapesFromWorkspace.dmm_gen_mixing.root@g"`

done | runParallel.py -n 8


# plotting

if [ -x "$(command -v makePlots_prefitPostfitPlots.py)" ]
then
#	for SHAPES in `ls $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/postFitShapesFromWorkspace.dmm_gen_mixing.root 2> /dev/null`; do

#		echo ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -i ${SHAPES} \
#			-b ZTT_GEN_DM_ZERO ZTT_GEN_DM_ONE ZTT_GEN_DM_TWO ZTT_GEN_DM_TEN ZTT_GEN_DM_ELEVEN "\"ZLL ZL ZJ\"" "\"TT TTT TTJ\"" W "\"VV VVT VVJ EWKZ\"" QCD \
#			--polarisation -r -a "\" --formats pdf png --x-label mt_m_2 --y-subplot-lims 0.5 1.5\"" \
#			--www $2/`echo ${SHAPES} | sed -e "s@${1}/@@g" -e "s@postFitShapesFromWorkspace.dmm_gen_mixing.root@@g"`/gen_mixing

#	done | runParallel.py -n 8
	
	for SHAPES in `ls $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/postFitShapesFromWorkspace.dmm_reco_mixing.root 2> /dev/null`; do

		echo ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -i ${SHAPES} \
			-b ZTT_GEN_DM_ZERO ZTT_GEN_DM_ONE ZTT_GEN_DM_TWO ZTT_GEN_DM_TEN ZTT_GEN_DM_ELEVEN "\"ZLL ZL ZJ\"" "\"TT TTT TTJ\"" W "\"VV VVT VVJ EWKZ\"" QCD \
			--polarisation -r -a "\" --formats pdf png --x-label mt_m_2 --y-subplot-lims 0.5 1.5\"" \
			--www $2/`echo ${SHAPES} | sed -e "s@${1}/@@g" -e "s@postFitShapesFromWorkspace.dmm_reco_mixing.root@@g"`/reco_mixing -n 8

	done # | runParallel.py -n 8
	
	for SHAPES in `ls $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/postFitShapesFromWorkspace.dmm_gen_mixing.root 2> /dev/null`; do

		echo ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -i ${SHAPES} \
			-b ZTT_GEN_DM_ZERO ZTT_GEN_DM_ONE ZTT_GEN_DM_TWO ZTT_GEN_DM_TEN ZTT_GEN_DM_ELEVEN "\"ZLL ZL ZJ\"" "\"TT TTT TTJ\"" W "\"VV VVT VVJ EWKZ\"" QCD \
			--polarisation -r -a "\" --formats pdf png --x-label mt_m_2 --y-subplot-lims 0.5 1.5\"" \
			--www $2/`echo ${SHAPES} | sed -e "s@${1}/@@g" -e "s@postFitShapesFromWorkspace.dmm_gen_mixing.root@@g"`/gen_mixing -n 8

	done # | runParallel.py -n 8
fi

