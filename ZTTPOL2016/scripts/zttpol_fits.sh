#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# ===== r floating ================================================================================

# combine

# best fit parameters saved into workspace
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 \
	--saveWorkspace -n .pol.best_fit \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# total uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 --algo singles \
	--snapshotName MultiDimFit -w w --saveWorkspace -n .pol.tot_unc \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.best_fit.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# statistical uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 1 --algo singles \
	--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .pol.stat_unc \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.best_fit.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# plotting

if [ -x "$(command -v higgsplot.py)" ]
then
	for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.tot_unc.MultiDimFit.mH0.root; do

		# full range
		echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_tot_stat_unc.json \
			-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` \
			-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -1.0 1.0 --title \"r floating\" --y-grid \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename best_fit_pol_tot_stat_unc --formats pdf png \
			--no-cache
	
		# zoomed
		echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_tot_stat_unc.json \
			-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol.tot_unc.MultiDimFit.mH0.root@@g"` \
			-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -0.3 0.0 --title \"r floating\" --y-grid \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename best_fit_pol_tot_stat_unc_zoom --formats pdf png \
			--no-cache

	done | runParallel.py -n 8
fi


# ===== r=1 fixed =================================================================================

# combine

# best fit parameters saved into workspace
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 0 --setParameters "r=1.0" --freezeParameters r \
	--saveWorkspace -n .pol_r1.best_fit \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# total uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 0 --setParameters "r=1.0" --freezeParameters r --algo singles \
	--snapshotName MultiDimFit -w w --saveWorkspace -n .pol_r1.tot_unc \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.best_fit.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# statistical uncertainty
combineTool.py -M MultiDimFit --redefineSignalPOIs r,pol -P pol --floatOtherPOIs 0 --setParameters "r=1.0" --freezeParameters r --algo singles \
	--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .pol_r1.stat_unc \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.best_fit.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# plotting

if [ -x "$(command -v higgsplot.py)" ]
then
	for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root; do

		# full range
		echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_r1_tot_stat_unc.json \
			-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` \
			-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -1.0 1.0 --title \"r=1 fixed\" --y-grid \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename best_fit_pol_r1_tot_stat_unc --formats pdf png \
			--no-cache
	
		# zoomed
		echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_r1_tot_stat_unc.json \
			-d `echo ${COMBINE_OUTPUT} | sed -e "s@higgsCombine.pol_r1.tot_unc.MultiDimFit.mH0.root@@g"` \
			-x 2 --x-lims 0 3 --x-ticks 2 --x-tick-labels \" \" --x-label \"\" --y-lims -0.3 0.0 --title \"r=1 fixed\" --y-grid \
			--www $2/`dirname ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g"` \
			--filename best_fit_pol_r1_tot_stat_unc_zoom --formats pdf png \
			--no-cache

	done | runParallel.py -n 8
fi


# ===== comparisons ===============================================================================

if [ -x "$(command -v higgsplot.py)" ]
then
	# channel comparison
	annotate-trees.py $1/*/datacards/combined/higgsCombine*.root -t limit -b channel channel_category --values 0 0
	
	annotate-trees.py $1/*/datacards/channel/mt/higgsCombine*.root -t limit -b channel channel_category --values 1 1
	annotate-trees.py $1/*/datacards/channel/et/higgsCombine*.root -t limit -b channel channel_category --values 2 5
	annotate-trees.py $1/*/datacards/channel/em/higgsCombine*.root -t limit -b channel channel_category --values 3 9
	annotate-trees.py $1/*/datacards/channel/tt/higgsCombine*.root -t limit -b channel channel_category --values 4 10
	
	annotate-trees.py $1/*/datacards/individual/mt/mt_rho/higgsCombine*.root -t limit -b channel channel_category --values 1 2
	annotate-trees.py $1/*/datacards/individual/mt/mt_a1/higgsCombine*.root -t limit -b channel channel_category --values 1 3
	annotate-trees.py $1/*/datacards/individual/mt/mt_oneprong/higgsCombine*.root -t limit -b channel channel_category --values 1 4
	annotate-trees.py $1/*/datacards/individual/et/et_rho/higgsCombine*.root -t limit -b channel channel_category --values 1 6
	annotate-trees.py $1/*/datacards/individual/et/et_a1/higgsCombine*.root -t limit -b channel channel_category --values 1 7
	annotate-trees.py $1/*/datacards/individual/et/et_oneprong/higgsCombine*.root -t limit -b channel channel_category --values 1 8
	annotate-trees.py $1/*/datacards/individual/tt/tt_rho/higgsCombine*.root -t limit -b channel channel_category --values 1 11
	annotate-trees.py $1/*/datacards/individual/tt/tt_combined_a1_a1/higgsCombine*.root -t limit -b channel channel_category --values 1 12
	annotate-trees.py $1/*/datacards/individual/tt/tt_combined_a1_oneprong/higgsCombine*.root -t limit -b channel channel_category --values 1 13
	annotate-trees.py $1/*/datacards/individual/tt/tt_combined_oneprong_oneprong/higgsCombine*.root -t limit -b channel channel_category --values 1 14

	for DIRECTORY in $1/*/datacards
	do
		for POL_OPTION in "pol" "pol_r1"
		do
			for ZOOM_OPTION in " --y-lims -1 1" "_zoom --y-lims -0.3 0"
			do
				echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_${POL_OPTION}_over_channel_tot_stat_unc.json \
					-d "\"${DIRECTORY}/combined ${DIRECTORY}/channel/mt ${DIRECTORY}/channel/et ${DIRECTORY}/channel/em ${DIRECTORY}/channel/tt\"" \
					--x-ticks 0 1 2 3 4 --x-tick-labels comb. channel_mt_large channel_et_large channel_em_large channel_tt_large --x-lims -0.5 4.5 \
					--www $2/`echo ${DIRECTORY} | sed -e "s@${1}/@@g"`/combined --formats pdf png --y-grid \
					--filename best_fit_${POL_OPTION}_over_channel_tot_stat_unc${ZOOM_OPTION} \
					--no-cache
			done
		done
	done | runParallel.py -n 8
	
	for DIRECTORY in $1/*/datacards
	do
		for POL_OPTION in "pol" "pol_r1"
		do
			for ZOOM_OPTION in " --x-lims -1 1" "_zoom --x-lims -0.3 0"
			do
				echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_${POL_OPTION}_over_channel_tot_stat_unc_rotated.json \
					-d "\"${DIRECTORY}/combined ${DIRECTORY}/channel/mt ${DIRECTORY}/channel/et ${DIRECTORY}/channel/em ${DIRECTORY}/channel/tt\"" \
					--y-ticks 0 1 2 3 4 --y-tick-labels comb. channel_mt_large channel_et_large channel_em_large channel_tt_large --y-lims -0.5 4.5 \
					--www $2/`echo ${DIRECTORY} | sed -e "s@${1}/@@g"`/combined --formats pdf png --x-grid \
					--filename best_fit_${POL_OPTION}_over_channel_tot_stat_unc_rotated${ZOOM_OPTION} \
					--no-cache
			done
		done
	done | runParallel.py -n 8

	for DIRECTORY in $1/*/datacards
	do
		for POL_OPTION in "pol" "pol_r1"
		do
			for ZOOM_OPTION in " --y-lims -1 1" "_zoom --y-lims -0.3 0"
			do
				echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_${POL_OPTION}_over_channel_category_tot_stat_unc.json \
					-d "\"${DIRECTORY}/combined \
					${DIRECTORY}/channel/mt ${DIRECTORY}/individual/mt/mt_rho ${DIRECTORY}/individual/mt/mt_a1 ${DIRECTORY}/individual/mt/mt_oneprong \
					${DIRECTORY}/channel/et ${DIRECTORY}/individual/et/et_rho ${DIRECTORY}/individual/et/et_a1 ${DIRECTORY}/individual/et/et_oneprong \
					${DIRECTORY}/channel/em \
					${DIRECTORY}/channel/tt ${DIRECTORY}/individual/tt/tt_rho ${DIRECTORY}/individual/tt/tt_combined_a1_a1 ${DIRECTORY}/individual/tt/tt_combined_a1_oneprong ${DIRECTORY}/individual/tt/tt_combined_oneprong_oneprong\"" \
					--x-ticks 0 1 2 3 4 5 6 7 8 9 0 10 12 11 13 14 --x-lims -0.5 14.5 --x-tick-labels comb. \
					channel_mt_large channel_mt_rho_large channel_mt_a1_large channel_mt_oneprong_large \
					channel_et_large channel_et_rho_large channel_et_a1_large channel_et_oneprong_large \
					channel_em_large \
					channel_tt_large channel_tt_rho_large channel_tt_combined_a1_a1_large channel_tt_combined_a1_oneprong_large channel_tt_combined_oneprong_oneprong_large \
					--www $2/`echo ${DIRECTORY} | sed -e "s@${1}/@@g"`/combined --formats pdf png --y-grid \
					--filename best_fit_${POL_OPTION}_over_channel_category_tot_stat_unc${ZOOM_OPTION} \
					--no-cache
			done
		done
	done | runParallel.py -n 8

	for DIRECTORY in $1/*/datacards
	do
		for POL_OPTION in "pol" "pol_r1"
		do
			for ZOOM_OPTION in " --x-lims -1 1" "_zoom --x-lims -0.3 0"
			do
				echo higgsplot.py -j ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_${POL_OPTION}_over_channel_category_tot_stat_unc_rotated.json \
					-d "\"${DIRECTORY}/combined \
					${DIRECTORY}/channel/mt ${DIRECTORY}/individual/mt/mt_rho ${DIRECTORY}/individual/mt/mt_a1 ${DIRECTORY}/individual/mt/mt_oneprong \
					${DIRECTORY}/channel/et ${DIRECTORY}/individual/et/et_rho ${DIRECTORY}/individual/et/et_a1 ${DIRECTORY}/individual/et/et_oneprong \
					${DIRECTORY}/channel/em \
					${DIRECTORY}/channel/tt ${DIRECTORY}/individual/tt/tt_rho ${DIRECTORY}/individual/tt/tt_combined_a1_a1 ${DIRECTORY}/individual/tt/tt_combined_a1_oneprong ${DIRECTORY}/individual/tt/tt_combined_oneprong_oneprong\"" \
					--y-ticks 0 1 2 3 4 5 6 7 8 9 0 10 12 11 13 14 --y-lims -0.5 14.5 --y-tick-labels comb. \
					channel_mt_large channel_mt_rho_large channel_mt_a1_large channel_mt_oneprong_large \
					channel_et_large channel_et_rho_large channel_et_a1_large channel_et_oneprong_large \
					channel_em_large \
					channel_tt_large channel_tt_rho_large channel_tt_combined_a1_a1_large channel_tt_combined_a1_oneprong_large channel_tt_combined_oneprong_oneprong_large \
					--www $2/`echo ${DIRECTORY} | sed -e "s@${1}/@@g"`/combined --formats pdf png --x-grid \
					--filename best_fit_${POL_OPTION}_over_channel_category_tot_stat_unc_rotated${ZOOM_OPTION} \
					--no-cache
			done
		done
	done | runParallel.py -n 8
fi
