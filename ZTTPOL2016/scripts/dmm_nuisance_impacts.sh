#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


for WORKSPACE in `ls $1/reco_dmm_data/datacards/individual/mt/mt_a1/workspace_reco_mixing.root $1/workspace_reco_mixing.root 2> /dev/null`
do
	for POI in x10; # x0 x1 x10;
	do
		pushd `dirname ${WORKSPACE}`

echo 1
		# initial fit
		combineTool.py -M Impacts --doInitialFit --allPars \
			--robustFit 1 -t -1 \
			--setParameters r=1 --freezeParameters r,x0,x1 \
			--redefineSignalPOIs x0,x1,x10 -P ${POI} \
			-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
echo 2
		# fits for all nuisance parameters
		combineTool.py -M Impacts --doFits --allPars \
			--robustFit 1 -t -1 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --setRobustFitAlgo Minuit2,Migrad \
			--setParameters r=1 --freezeParameters r,x0,x1 \
			--redefineSignalPOIs x0,x1,x10 -P ${POI} \
			-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
echo 3
		# collect results
		combineTool.py -M Impacts --allPars \
			--setParameters r=1 --freezeParameters r,x0,x1 \
			--redefineSignalPOIs x0,x1,x10 -P ${POI} \
			-m 0 -d `basename ${WORKSPACE}` -o impacts.${POI}.json --parallel 8
	
echo 4
		# plot results
		plotImpacts.py -i impacts.${POI}.json -o impacts.${POI}
	
echo 5
		popd
	
		if [ -x "$(command -v www_publish.py)" ]
		then
			if [ ! -d websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`/reco_mixing ]
			then
				mkdir -p websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`/reco_mixing
			fi
		
			cp `echo ${WORKSPACE} | sed -e "s@workspace.root@impacts.${POI}.*@g"` websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`/reco_mixing
		
			${CMSSW_BASE}/src/Artus/HarryPlotter/scripts/www_publish.py \
					-i websync/`date +%Y_%m_%d`/$2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`/reco_mixing \
					-o $2/`dirname ${WORKSPACE} | sed -e "s@${1}/@@g"`
		fi
	done
done

