#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


export POIS="r,x0,x1,x10" #,x2,x11"

# combine

for POI in `echo ${POIS} | tr "," "\n"`;
do

	# best fit parameters saved into workspace
	combineTool.py -M MultiDimFit --redefineSignalPOIs ${POIS} -P ${POI} --floatOtherPOIs 1 \
		--saveWorkspace -n .dmm.best_fit.scan.${POI} \
		-d $1/*/datacards/{channel/*,combined}/workspace.root \
		--there -m 0 --parallel 8 \
		--robustFit 1

	# total uncertainty
	combineTool.py -M MultiDimFit --redefineSignalPOIs ${POIS} -P ${POI} --floatOtherPOIs 1 --algo grid --points 200 \
		--snapshotName MultiDimFit -w w --saveWorkspace -n .dmm.tot_unc.scan.${POI} \
		-d $1/*/datacards/{channel/*,combined}/higgsCombine.dmm.best_fit.scan.${POI}.MultiDimFit.mH0.root \
		--there -m 0 --parallel 8 \
		--robustFit 1

	# statistical uncertainty
	combineTool.py -M MultiDimFit --redefineSignalPOIs ${POIS} -P ${POI} --floatOtherPOIs 1 --algo grid --points 200 \
		--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .dmm.stat_unc.scan.${POI} \
		-d $1/*/datacards/{channel/*,combined}/higgsCombine.dmm.best_fit.scan.${POI}.MultiDimFit.mH0.root \
		--there -m 0 --parallel 8 \
		--robustFit 1

	# plotting

	if [ -x "$(command -v higgsplot.py)" ]
	then
		for COMBINE_OUTPUT in $1/*/datacards/{channel/*,combined}/higgsCombine.dmm.tot_unc.scan.${POI}.MultiDimFit.mH0.root; do
	
			# full range
			echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.dmm.tot_unc.scan.${POI}.MultiDimFit.mH0.root@higgsCombine.dmm.stat_unc.scan.${POI}.MultiDimFit.mH0.root@g"` \
				-f limit -x ${POI} -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --y-lims 0 100 \
				--x-label "\"Parameter `echo ${POI} | sed -e s@x@x_{@g`}\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				-m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
				--labels \"Stat. + Syst.\" \"\" \"\" \"\" \"Stat.\" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
				--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
				--filename higgsCombine.dmm.scan.${POI}.MultiDimFit.mH0 --formats pdf png \
				--no-cache
			
			# full range with fit
			echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.dmm.tot_unc.scan.${POI}.MultiDimFit.mH0.root@higgsCombine.dmm.stat_unc.scan.${POI}.MultiDimFit.mH0.root@g"` --nicks stat tot \
				-f limit -x ${POI} -y \"2*deltaNLL\" --tree-draw-options TGraph --y-lims 0 100 \
				--analysis-modules FunctionFit --functions "(x>=[0])*([1]*([0]-x)^2)+(x<[0])*([2]*([0]-x)^2)" --function-nicknames statfit totfit --function-parameters "\"0 1000 1000\"" --function-fit stat tot \
				--x-label "\"Parameter `echo ${POI} | sed -e s@x@x_{@g`}\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				-m P P L L --marker-sizes 0.5 --line-styles 1 -C 1 2 1 2 \
				--labels \"Stat. + Syst.\" \"Stat.\" \"\" \"\" --legend-markers P --legend 0.32 0.72 0.7 0.9 \
				--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
				--filename higgsCombine.dmm.scan.${POI}.MultiDimFit.mH0_fit --formats pdf png \
				--no-cache
			
			# zoomed
			echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.dmm.tot_unc.scan.${POI}.MultiDimFit.mH0.root@higgsCombine.dmm.stat_unc.scan.${POI}.MultiDimFit.mH0.root@g"` \
				-f limit -x ${POI} -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -0.1 0.1 --y-lims 0 10 \
				--x-label "\"Parameter `echo ${POI} | sed -e s@x@x_{@g`}\"" --y-label "\"Likelihood -2#Deltaln L\"" \
				-m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
				--labels \"Stat. + Syst.\" \"\" \"\" \"\" \"Stat.\" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
				--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
				--filename higgsCombine.dmm.scan.${POI}.MultiDimFit.mH0_zoom --formats pdf png \
				--no-cache

		done | runParallel.py -n 8
	fi

done
