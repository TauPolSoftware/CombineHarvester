#!/bin/sh

# Mandatory options
# $1: artus output directory
# $2: datacards output base directory
# $3: www base directory


$CMSSW_BASE/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_datacards.sh $1 $2
$CMSSW_BASE/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_scans.sh $2 $3
$CMSSW_BASE/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_scan_comparison.sh $2 $3
$CMSSW_BASE/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_fits.sh $2 $3
$CMSSW_BASE/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_prefit_postfit_plots.sh $2 $3
$CMSSW_BASE/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_nuisance_impacts.sh $2 $3
#$CMSSW_BASE/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_unblinding.sh $1 $2 $3

