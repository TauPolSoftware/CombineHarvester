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
combineTool.py -M T2W -i <output_dir>/datacards/{individual/*/*,category/*,channel/*,combined}/ztt*13TeV.txt -o workspace.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol --parallel 8
```

## Fitting

```bash
combineTool.py -M MultiDimFit -d <output_dir>/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --algo singles -P pol --redefineSignalPOIs pol --there --parallel 8
```
