#!/bin/sh

# Mandatory options
# $1: datacards output base directory


for WORKSPACE in `ls $1/best_choice/datacards/combined/workspace.root $1/workspace.root 2> /dev/null`
do
	pushd `dirname ${WORKSPACE}`
	
	# initial fit
	combineTool.py -M Impacts --doInitialFit --allPars \
		--redefineSignalPOIs pol --setParameters pol=-0.159,r=1 --setParameterRanges pol=-0.2,-0.1:r=0.5,1.5 \
		--robustFit 1 -t -1 \
		-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
	# fits for all nuisance parameters
	combineTool.py -M Impacts --doFits --allPars \
		--redefineSignalPOIs pol --setParameters pol=-0.159,r=1 --setParameterRanges pol=-0.2,-0.1:r=0.5,1.5 \
		--robustFit 1 -t -1 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --setRobustFitAlgo Minuit2,Migrad \
		-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
	# collect results
	combineTool.py -M Impacts --allPars \
		--redefineSignalPOIs pol --setParameters pol=-0.159,r=1 --setParameterRanges pol=-0.2,-0.1:r=0.5,1.5 \
		-m 0 -d `basename ${WORKSPACE}` -o impacts.json --parallel 8
	
	# plot results
	plotImpacts.py -i impacts.json -o impacts
	
	popd
done

