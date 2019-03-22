#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


for WORKSPACE in `ls $1/best_choice/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root $1/workspace.root 2> /dev/null`
do
	pushd `dirname ${WORKSPACE}`
	
	# initial fit
	combineTool.py -M Impacts --doInitialFit --allPars \
		--redefineSignalPOIs pol --setParameterRanges r=0.5,1.5:pol=-0.8,0.5 --setParameters r=1,pol=-0.2308 \
		--robustFit 1 \
		-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
	# fits for all nuisance parameters
	combineTool.py -M Impacts --doFits --allPars \
		--redefineSignalPOIs pol --setParameterRanges r=0.5,1.5:pol=-0.8,0.5 --setParameters r=1,pol=-0.2308 \
		--robustFit 1 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --setRobustFitAlgo Minuit2,Migrad \
		-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
	# collect results
	combineTool.py -M Impacts --allPars \
		--redefineSignalPOIs pol --setParameterRanges r=0.5,1.5:pol=-0.8,0.5 --setParameters r=1,pol=-0.2308 \
		-m 0 -d `basename ${WORKSPACE}` -o impacts.json --parallel 8
	
	# plot results
	plotImpacts.py -i impacts.json -o impacts
	
	popd
	
	if [ -x "$(command -v www_publish.py)" ]
	then
		if [ ! -d websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"` ]
		then
			mkdir -p websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`
		fi
		
		cp `echo ${WORKSPACE} | sed -e "s@workspace.root@impacts.*@g"` websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`
		
		${CMSSW_BASE}/src/Artus/HarryPlotter/scripts/www_publish.py \
				-i websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"` \
				-o $2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`
	fi
done

