#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# combine

# total uncertainty
#combineTool.py -M MultiDimFit --algo singles \
#	--saveWorkspace -n .dmm_gen_mixing \
#	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace_gen_mixing.root \
#	--there -m 0 --parallel 1 \
#	--robustFit 1

combineTool.py -M MultiDimFit --algo singles \
	--saveWorkspace -n .dmm_reco_mixing \
	-d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace_reco_mixing.root \
	--there -m 0 --parallel 1 \
	--robustFit 1

## best fit parameters saved into workspace
#combineTool.py -M MultiDimFit \
#	--setParameterRanges r=0.8,1.2:x0=-0.2,0.2:x1=-0.2,0.2:x2=-0.2,0.2:x10=-0.2,0.2:x11=-1.0,1.0 \
#	--saveWorkspace -n .dmm.best_fit \
#	-d $1/*/datacards/{channel/*,combined}/workspace.root \
#	--there -m 0 --parallel 8 \
#	--robustFit 1

## total uncertainty
#combineTool.py -M MultiDimFit --algo singles \
#	--setParameterRanges r=0.8,1.2:x0=-0.2,0.2:x1=-0.2,0.2:x2=-0.2,0.2:x10=-0.2,0.2:x11=-1.0,1.0 \
#	--snapshotName MultiDimFit -w w --saveWorkspace -n .dmm.tot_unc \
#	-d $1/*/datacards/{channel/*,combined}/higgsCombine.dmm.best_fit.MultiDimFit.mH0.root \
#	--there -m 0 --parallel 8 \
#	--robustFit 1

## statistical uncertainty
#combineTool.py -M MultiDimFit --algo singles \
#	--setParameterRanges r=0.8,1.2:x0=-0.2,0.2:x1=-0.2,0.2:x2=-0.2,0.2:x10=-0.2,0.2:x11=-1.0,1.0 \
#	--snapshotName MultiDimFit -w w --saveWorkspace --freezeNuisanceGroups syst_plus_bbb -n .dmm.stat_unc \
#	-d $1/*/datacards/{channel/*,combined}/higgsCombine.dmm.best_fit.MultiDimFit.mH0.root \
#	--there -m 0 --parallel 8 \
#	--robustFit 1

