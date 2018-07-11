#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# ===== r floating ================================================================================

# combine

# best fit parameters saved into workspace
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 \
	--saveWorkspace -n .pol.best_fit.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# total uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 --algo grid --points 200 \
	--snapshotName MultiDimFit -w w --saveWorkspace -n .pol.tot_unc.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.best_fit.scan.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# statistical uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 --algo grid --points 200 \
	--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .pol.stat_unc.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.best_fit.scan.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# plotting

if [ -x "$(command -v higgsplot.py)" ]
then
	for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root; do
	
		# full range
		echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol.stat_unc.scan.MultiDimFit.mH0.root@g"` \
			-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -1 1 --y-lims 0 100 \
			--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r floating\"" \
			-m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
			--labels \"Stat. + Syst.\" \"\" \"\" \"\" \"Stat.\" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename higgsCombine.pol.scan.MultiDimFit.mH0 --formats pdf png \
			--no-cache
	
		# zoomed
		echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol.stat_unc.scan.MultiDimFit.mH0.root@g"` \
			-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -0.3 0 --y-lims 0 10 \
			--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r floating\"" \
			-m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
			--labels "\"Stat. + Syst.\"" \"\" \"\" \"\" "\"Stat.\"" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename higgsCombine.pol.scan.MultiDimFit.mH0_zoom --formats pdf png \
			--no-cache

	done | runParallel.py -n 8
fi


# ===== r=1 fixed =================================================================================

# combine

# best fit parameters saved into workspace
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 0 --setParameters "r=0.98" --freezeParameters r \
	--saveWorkspace -n .pol_r1.best_fit.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# total uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 0 --setParameters "r=0.98" --freezeParameters r --algo grid --points 200 \
	--snapshotName MultiDimFit -w w --saveWorkspace -n .pol_r1.tot_unc.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.best_fit.scan.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# statistical uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 0 --setParameters "r=0.98" --freezeParameters r --algo grid --points 200 \
	--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .pol_r1.stat_unc.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.best_fit.scan.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# plotting

if [ -x "$(command -v higgsplot.py)" ]
then
for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root; do
	
		# full range
		echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol_r1.stat_unc.scan.MultiDimFit.mH0.root@g"` \
			-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -1 1 --y-lims 0 100 \
			--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r=1 fixed\"" \
			-m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
			--labels \"Stat. + Syst.\" \"\" \"\" \"\" \"Stat.\" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename higgsCombine.pol_r1.scan.MultiDimFit.mH0 --formats pdf png \
			--no-cache
	
		# zoomed
		echo higgsplot.py -i ${COMBINE_OUTPUT} `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.scan.MultiDimFit.mH0.root@higgsCombine.pol_r1.stat_unc.scan.MultiDimFit.mH0.root@g"` \
			-f limit -x pol -y \"2*deltaNLL\" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -0.3 0 --y-lims 0 10 \
			--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Likelihood -2#Deltaln L\"" --title "\"r=1 fixed\"" \
			-m LP L L L LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 1 1 2 3 -C 1 1 1 1 2 2 2 2 \
			--labels "\"Stat. + Syst.\"" \"\" \"\" \"\" "\"Stat.\"" \"\" \"\" \"\" --legend-markers LP --legend 0.32 0.72 0.7 0.9 \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename higgsCombine.pol_r1.scan.MultiDimFit.mH0_zoom --formats pdf png \
			--no-cache

	done | runParallel.py -n 8
fi


# ===== 2D scans ==================================================================================

# combine

# total uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol --floatOtherPOIs 1 --algo grid --points 900 --setParameterRanges pol=-0.3,0:r=0.5,1.5 \
	--snapshotName MultiDimFit -w w --saveWorkspace -n .pol_r.tot_unc.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.best_fit.scan.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# statistical uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol --floatOtherPOIs 1 --algo grid --points 900 --fastScan --setParameterRanges pol=-0.3,0:r=0.5,1.5 \
	--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .pol_r.stat_unc.scan \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.best_fit.scan.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# plotting

if [ -x "$(command -v higgsplot.py)" ]
then
	for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r.tot_unc.scan.MultiDimFit.mH0.root; do
	
		echo higgsplot.py -i ${COMBINE_OUTPUT} -f limit \
			-x pol -y r -z \"2*deltaNLL\" --tree-draw-options prof --x-bins 30,-0.3,0.0 --y-bins 30,0.5,1.5  \
			--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Signal Strength r\"" --z-label "\"Likelihood -2#Deltaln L\"" \
			--title "\"Stat. + syst. uncertainties\"" -m COLZ --x-lims -0.3 0 --y-lims 0.5 1.5 --z-lims 0 10 \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename `basename ${COMBINE_OUTPUT} | sed -e "s@.root@_zoom@g"` --formats pdf png \
			--no-cache

	done | runParallel.py -n 8
	
	for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r.stat_unc.scan.MultiDimFit.mH0.root; do
	
		echo higgsplot.py -i ${COMBINE_OUTPUT} -f limit \
			-x pol -y r -z \"2*deltaNLL\" --tree-draw-options prof --x-bins 30,-0.3,0.0 --y-bins 30,0.5,1.5  \
			--x-label "\"Average Polarisation #LTP_{#tau}#GT\"" --y-label "\"Signal Strength r\"" --z-label "\"Likelihood -2#Deltaln L\"" \
			--title "\"Stat. uncertainties\"" -m COLZ --x-lims -0.3 0 --y-lims 0.5 1.5 --z-lims 0 10 \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename `basename ${COMBINE_OUTPUT} | sed -e "s@.root@_zoom@g"` --formats pdf png \
			--no-cache

	done | runParallel.py -n 8
fi

