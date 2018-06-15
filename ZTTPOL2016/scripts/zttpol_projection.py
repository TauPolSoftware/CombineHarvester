#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import CombineHarvester.CombineTools.ch as ch

import CombineHarvester.ZTTPOL2016.zttpol2016_functions as zttpol2016_functions
import CombineHarvester.ZTTPOL2016.zttpol2016_datacards as zttpol2016_datacards


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Datacard Projection")

	parser.add_argument("-d", "--datacards", nargs="+", required=True,
						help="Input datacards. The filenames have to match \"$ANALYSIS_$CHANNEL_$BINID_$ERA.txt\" and they should not contain combinations of channels/categories.")
	parser.add_argument("--in-lumi", type=float, default=35.87,
						help="Integrated luminosity of the inputs in 1/fb.")
	parser.add_argument("--out-lumis", type=int, nargs="+", default=[300.0, 3000.0],
						help="Integrated luminosity values the datacards should be projected to in 1/fb.")
	parser.add_argument("--combinations", nargs="+",
						default=["combined"],
						choices=["individual", "channel", "category", "combined"],
						help="Combinations to perform. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir", required=True,
						help="Output directory.")

	args = parser.parse_args()
	
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	datacard_filename_templates = []
	if "individual" in args.combinations:
		datacard_filename_templates.append("datacards/individual/${CHANNEL}/${BIN}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt")
	if "channel" in args.combinations:
		datacard_filename_templates.append("datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt")
	if "category" in args.combinations:
		datacard_filename_templates.append("datacards/category/${BINID}/${ANALYSIS}_${BIN}_${ERA}.txt")
	if "combined" in args.combinations:
		datacard_filename_templates.append("datacards/combined/${ANALYSIS}_${ERA}.txt")
	
	cb = ch.CombineHarvester()
	for datacard in args.datacards:
		cb.QuickParseDatacard(datacard, "$ANALYSIS_$CHANNEL_$BINID_$ERA.txt", True)
	
	for out_lumi in args.out_lumis:
		scale_factor = float(out_lumi) / args.in_lumi
		
		cb_copy = cb.deep()
		cb_copy.ForEachProc(lambda obj: obj.set_rate(obj.rate() * scale_factor))
		cb_copy.ForEachObs (lambda obj: obj.set_rate(obj.rate() * scale_factor))
	
		datacards = zttpol2016_datacards.ZttPolarisationDatacards(cb=cb_copy)
		for datacard_filename_template in datacard_filename_templates:
			zttpol2016_functions.WriteDatacard(
					datacards,
					datacard_filename_template.replace("{", "").replace("}", ""),
					output_root_filename_template.replace("{", "").replace("}", ""),
					os.path.join(args.output_dir, str(out_lumi))
			)

