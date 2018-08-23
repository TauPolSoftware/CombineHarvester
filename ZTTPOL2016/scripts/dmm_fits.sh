#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# combine

# best fit parameters saved into workspace
combineTool.py -M MultiDimFit \
	--saveWorkspace -n .dmm.best_fit \
	-d $1/*/datacards/combined/workspace.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# total uncertainty
combineTool.py -M MultiDimFit --algo singles \
	--snapshotName MultiDimFit -w w --saveWorkspace -n .dmm.tot_unc \
	-d $1/*/datacards/combined/higgsCombine.dmm.best_fit.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

# statistical uncertainty
combineTool.py -M MultiDimFit --algo singles \
	--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .dmm.stat_unc \
	-d $1/*/datacards/combined/higgsCombine.dmm.best_fit.MultiDimFit.mH0.root \
	--there -m 0 --parallel 8 \
	--robustFit 1

