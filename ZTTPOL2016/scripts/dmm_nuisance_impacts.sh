#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


for WORKSPACE in `ls $1/asimov_m_2/datacards/{channel/*,combined}/workspace.root $1/workspace.root 2> /dev/null`
do
	for POI in x0 x1 x2 x10 x11;
	do
		pushd `dirname ${WORKSPACE}`
	
		# initial fit
		combineTool.py -M Impacts --doInitialFit --allPars \
			--redefineSignalPOIs r,x0,x1,x2,x10,x11 -P ${POI} \
			--setParameterRanges r=0.8,1.2:x0=-0.2,0.2:x1=-0.2,0.2:x2=-0.2,0.2:x10=-0.2,0.2:x11=-1.0,1.0 \
			--robustFit 1 -t -1 \
			-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
		# fits for all nuisance parameters
		combineTool.py -M Impacts --doFits --allPars \
			--redefineSignalPOIs r,x0,x1,x2,x10,x11 -P ${POI} \
			--setParameterRanges r=0.8,1.2:x0=-0.2,0.2:x1=-0.2,0.2:x2=-0.2,0.2:x10=-0.2,0.2:x11=-1.0,1.0 \
			--robustFit 1 -t -1 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --setRobustFitAlgo Minuit2,Migrad \
			-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
		# collect results
		combineTool.py -M Impacts --allPars \
			--redefineSignalPOIs r,x0,x1,x2,x10,x11 -P ${POI} \
			--setParameterRanges r=0.8,1.2:x0=-0.2,0.2:x1=-0.2,0.2:x2=-0.2,0.2:x10=-0.2,0.2:x11=-1.0,1.0 \
			-m 0 -d `basename ${WORKSPACE}` -o impacts.${POI}.json --parallel 8
	
		# plot results
		plotImpacts.py -i impacts.${POI}.json -o impacts.${POI}
	
		popd
	
		if [ -x "$(command -v www_publish.py)" ]
		then
			if [ ! -d websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"` ]
			then
				mkdir -p websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`
			fi
		
			cp `echo ${WORKSPACE} | sed -e "s@workspace.root@impacts.${POI}.*@g"` websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`
		
			${CMSSW_BASE}/src/Artus/HarryPlotter/scripts/www_publish.py \
					-i websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"` \
					-o $2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`
		fi
	done
done

