 # -*- coding: utf-8 -*-

import CombineHarvester.CombineTools.ch as ch

class SystematicLibary(object):
    def __init__(self):

    ##----------------------------------------------------------lnN uncertanties----------------------------------------------------------##

        ##-------------------------------Luminosity-------------------------------##

        self.lumi_syst_args = [
            "lumi_$ERA",
            "lnN",
            ch.SystMap("era")
                (["7TeV", "8TeV"], 1.026)
                (       ["13TeV"], 1.027) # CMS-PAS-LUM-15-001
        ]
        self.lumi2016_syst_args = [
            "lumi_$ERA",
            "lnN",
            ch.SystMap("era")
                (       ["13TeV"], 1.025)

        ]
        ##-------------------------------Cross section-------------------------------##

        self.ztt_cross_section_syst_args = [
            "CMS_$ANALYSIS_zttNorm_$ERA",
            "lnN",
            ch.SystMap("era", "process")
                (["7TeV", "8TeV"], ["ZTT", "ZLL", "ZL", "ZJ"], 1.03)
                (       ["13TeV"], ["ZTT", "ZLL", "ZL", "ZJ"], 1.04)
        ]
        self.zll_cross_section_syst_args = [
            "CMS_$ANALYSIS_zjXsec_$ERA",
            "lnN",
            ch.SystMap("era", "process")
                (       ["13TeV"], ["ZLL", "ZL", "ZJ"], 1.04) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
        ]

        ##-------------------------------Efficiencies-------------------------------##

        self.trigger_efficiency2016_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L76-L88
            "CMS_eff_trigger_$CHANNEL_$ERA",
            "lnN",
            ch.SystMap("era", "channel")
                (["13TeV"], ["mt", "et"], 1.02)
                (["13TeV"], ["tt"], 1.10)
        ]
        self.trigger_efficiency2016_em_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L82-L84
            "CMS_eff_trigger_em_$ERA",
            "lnN",
            ch.SystMap("era", "channel")
                (["13TeV"], ["em", "ttbar"], 1.02)
        ]
        self.electron_efficiency_syst_args = [
            "CMS_eff_e",
            "lnN",
            ch.SystMap("era")
                (["7TeV", "8TeV"], 1.02)
                (       ["13TeV"], 1.04) # https://github.com/cms-analysis/CombineHarvester/blob/HIG15007/HIG15007/scripts/setupDatacards.py#L107-L110
        ]
        self.electron_efficiency2016_syst_args = [
            "CMS_eff_e",
            "lnN",
            ch.SystMap("era")
                (       ["13TeV"], 1.02) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
        ]
        self.muon_efficiency_syst_args = [
            "CMS_eff_m",
            "lnN",
            ch.SystMap("era")
                (["7TeV", "8TeV"], 1.02)
                (       ["13TeV"], 1.03) # https://github.com/cms-analysis/CombineHarvester/blob/HIG15007/HIG15007/scripts/setupDatacards.py#L101-L105
        ]
        self.muon_efficiency2016_syst_args = [
            "CMS_eff_m",
            "lnN",
            ch.SystMap("era")
                (       ["13TeV"], 1.02) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
        ]
        self.tau_efficiency_corr_syst_args = [
            "CMS_eff_t_$ERA",
            "lnN",
            ch.SystMap("era", "channel")
                (["7TeV", "8TeV"], ["mt", "et"], 1.08)
                (["7TeV", "8TeV"], ["tt"],       1.19)
                (       ["13TeV"], ["mt", "et", "tt"], 1.05) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
        ]
        self.tau_efficiency_syst_args = [
            "CMS_eff_t_$CHANNEL_$ERA",
            "lnN",
            ch.SystMap("era", "channel")
                (["7TeV", "8TeV"], ["mt", "et"], 1.08)
                (["7TeV", "8TeV"], ["tt"],       1.19)
                (       ["13TeV"], ["mt", "et", "tt"], 1.03) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
        ]

        ##-------------------------------Scale-------------------------------##

        self.met_scale_syst_args = [
            "CMS_$ANALYSIS_scale_met_$ERA",
            "lnN",
            ch.SystMap("era", "process")
                (["13TeV"], ["ggH", "qqH", "WH", "ZH", "VH"], 0.98) # copied from 8TeV
                (["13TeV"], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TTJJ", "TTT", "TT", "VV", "WJ", "W"], 1.03) # copied from 8TeV
        ]
        self.boson_scale_met_syst_args = [
            "CMS_$ANALYSIS_boson_scale_met",
            "lnN",
            ch.SystMap("channel")
                (["mt"], 1.02)
        ]
        self.ewk_top_scale_met_syst_args = [
            "CMS_$ANALYSIS_ewkTop_scale_met",
            "lnN",
            ch.SystMap("channel")
                (["mt"], 1.03)
        ]

        ##-------------------------------Resolution-------------------------------##

        self.boson_resolution_met_syst_args = [
            "CMS_$ANALYSIS_boson_reso_met",
            "lnN",
            ch.SystMap("channel")
                (["mt"], 1.02)
        ]
        self.ewk_top_resolution_met_syst_args = [
            "CMS_$ANALYSIS_ewkTop_reso_met",
            "lnN",
            ch.SystMap("channel")
                (["mt"], 1.01)
        ]

        ##-------------------------------Fake rate-------------------------------##

        self.eFakeTau2016_syst_args = [
            "CMS_$ANALYSIS_eFakeTau_$ERA",
            "lnN",
            ch.SystMap("era", "process")
                (       ["13TeV"], ["ZLL", "ZL"], 1.12) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
        ]
        self.muFakeTau_syst_args = [
            "CMS_$ANALYSIS_mFakeTau_$ERA",
            "lnN",
            ch.SystMap("era", "process",)
                (       ["13TeV"], ["ZLL", "ZL"], 2.00) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
        ]
        self.muFakeTau2016_syst_args = [
            "CMS_$ANALYSIS_mFakeTau_$ERA",
            "lnN",
            ch.SystMap("era", "process",)
                (       ["13TeV"], ["ZLL", "ZL"], 1.25) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
        ]
        self.zjFakeTau_syst_args = [
            "CMS_$ANALYSIS_zjFakeTau_$ERA",
            "lnN",
            ch.SystMap("era", "process",)
                (       ["13TeV"], ["ZLL", "ZL"], 1.30) # From Yuta's polarisation analysis
        ]
        self.jetFakeTau_syst_args = [
            "CMS_$ANALYSIS_jetFakeTau_$ERA",
            "lnN",
            ch.SystMap("era", "process",)
                (       ["13TeV"], ["ZJ", "TTJJ", "VVJ"], 1.20)
        ]

    ##----------------------------------------------------------Shape uncertanties----------------------------------------------------------##
