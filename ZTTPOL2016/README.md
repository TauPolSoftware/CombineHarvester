# Creating Datacards for 2016 polarisation analysis

Check out CH with the correct branch:
```
git clone --recursive git@github.com:TauPolSoftware/CombineHarvester.git CombineHarvester -b ZTTPOL2016
```

The morphing script `scripts/zttpol2016.py` is structured into functions for creating the datacard from `python/zttpol2016_datacards.py`

It can be called by:

```
zttpol2016.py -i <input_dir> -o <output_dir> -c <channel> --categories <categories> -c <channel> --categories <categories>
```

The script looks in <input_dir> for the samples to extract shapes from. The format for the sample files is:

```
ztt_<channel>_<channel>_<categorie>_<era>.root
```

## Text2Workspace

```bash
combineTool.py -M T2W -o workspace.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol -m 0 -i <output_dir>/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt --parallel 8
```

## Fitting

### General

The physics model has 2 parameters:
- The (unbiased) average tau polarisation called `pol` and defined in the range -1 to 1
- The total Z->tautau signal strength called `r`. The default value is 1 and its range is set to 0 to 5.

Fitting the polarisation and leaving the signal strength as a freely floating parameter is done with
```bash
--redefineSignalPOIs pol
```
In order to fix the signal strength to 1, one should add the option
```bash
--freezeParameters r
```

### Simple MultiDimFit

```bash
combineTool.py -M MultiDimFit --algo singles -P pol --redefineSignalPOIs pol --there -m 0 -d <output_dir>/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8
```

### Likelihood scan for polarisation (1D)
```bash
combineTool.py -M MultiDimFit --points 100 --redefineSignalPOIs pol --algo grid --there -n .pol -m 0 -d <output_dir>/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8 # --setPhysicsModelParameterRanges pol=-1,1
combineTool.py -M MultiDimFit --points 100 --redefineSignalPOIs pol --freezeParameters r --algo grid --there -n .pol_r1 -m 0 -d <output_dir>/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8 # --setPhysicsModelParameterRanges pol=-1,1
```

### Likelihood scan for polarisation and signal strength (2D)

```bash
combineTool.py -M MultiDimFit --points 2500 --redefineSignalPOIs pol,r --algo grid --there -n .pol_r -m 0 -d <output_dir>/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8
```

### Trouble Shooting

#### Stable fitting options

More options to achieve more stable minimisations in the fits can be applied:
```bash
--robustFit 1 --preFitValue 1.0 --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo Minuit2 --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:1.0
```

