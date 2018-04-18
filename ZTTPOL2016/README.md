# Creating Datacards for 2016 polarisation analysis

The morphing script `scripts/zttpol2016.py` is structured into functions for creating the datacard from `python/zttpol2016_datacards.py`

It can be called by:

```
zttpol2016.py -i <input_dir> -o <output_dir> -c <channel> --categories <categories> -c <channel> --categories <categories>
```

The script looks in <input_dir> for the samples to extract shapes from. The format for the sample files is:

```
ztt_<channel>_<channel>_<categorie>_<era>.root
```
