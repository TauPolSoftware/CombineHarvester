#!/bin/sh

# Mandatory options
# $1: artus output directory
# $2: datacards output base directory
# $3: www base directory


# datacards

for MODE in --modify-asimov-polarisation --modify-unpolarisation-value;
do
	for POL in -0.35 -0.30 -0.25 -0.24 -0.23 -0.22 -0.21 -0.20 -0.19 -0.18 -0.17 -0.16 -0.15 -0.14 -0.13 -0.12 -0.11 -0.10 -0.05 -0.00;
#	for POL in -0.18 -0.17 -0.16;
	do
		$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsZttPolarisation.py \
				-i $1 -n 8 -o $2/best_choice_linearity_`echo ${MODE} | sed -e "s@--modify-@@g" -e "s@-@_@g"`_`echo ${POL} | sed -e "s@-@m@g" -e "s@\.@p@g"` --clear-output-dir --use-asimov-dataset --fixed-variables best_choice \
				-c em --categories em_combined_oneprong_oneprong \
				-c et --categories et_a1 et_rho et_oneprong \
				-c mt --categories mt_rho mt_a1 mt_oneprong \
				-c tt --categories tt_rho tt_combined_a1_a1 tt_combined_a1_oneprong tt_combined_oneprong_oneprong \
				${MODE} ${POL}
	done
done

combineTool.py -M T2W -o workspace.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol -m 0 --parallel 8 \
		-i $2/best_choice_linearity_*/datacards/combined/ztt*13TeV.txt


# combine

combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 --algo singles \
	--saveWorkspace -n .pol.linearity_fit \
	-d $2/best_choice_linearity_*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root \
	--there -m 0 --parallel 8 \
	--robustFit 1
	
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 --algo grid --points 76 \
	--setParameterRanges pol=-0.555,0.205 \
	--saveWorkspace -n .pol.linearity_scan \
	-d $2/best_choice_linearity_*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root \
	--there -m 0 --parallel 8 \
	--robustFit 1


# plotting

for OUTPUT in $2/best_choice_linearity_*/datacards/combined/higgsCombine.pol.linearity_*.MultiDimFit.mH0.root;
do
	echo annotate-trees.py ${OUTPUT} -t limit --values `echo ${OUTPUT} | sed -e "s@$2/best_choice_linearity_@@g" -e "s@asimov_polarisation@@g" -e "s@unpolarisation_value@@g" -e "s@/datacards/combined/higgsCombine.pol.linearity_.*.MultiDimFit.mH0.root@@g" -e "s@_@@g" -e "s@m0p@-0.@g" -e "s@0p@0.@g" -e "s@default@-999.0@g"` -b polarisation
done | runParallel.py -n 8

for MODE in --modify-asimov-polarisation --modify-unpolarisation-value;
do
	higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_polarisation.json \
		-i "$2/best_choice_linearity_$(echo ${MODE} | sed -e "s@--modify-@@g" -e "s@-@_@g")_*/datacards/combined/higgsCombine.pol.linearity_fit.MultiDimFit.mH0.root" \
		--www $3/best_choice_linearity/datacards/combined --filename linearity_check_fit_`echo ${MODE} | sed -e "s@--modify-@@g" -e "s@-@_@g"` --formats pdf png --grid \
		--redo-cache

	higgsplot.py --www $3/best_choice_linearity/datacards/combined --filename linearity_check_scan_`echo ${MODE} | sed -e "s@--modify-@@g" -e "s@-@_@g"` --formats pdf png --grid \
		-i $2/best_choice_linearity_`echo ${MODE} | sed -e "s@--modify-@@g" -e "s@-@_@g"`_*/datacards/combined/higgsCombine.pol.linearity_scan.MultiDimFit.mH0.root \
		-f limit -x pol -y deltaNLL --tree-draw-options TGraph -m PL -w "quantileExpected>-0.999" \
		--redo-cache
done

