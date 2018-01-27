# clean-alignment
## clean-alignment: a new tool to clean and remove outliers from multiple sequence alignment

Clean-alignment is a simple tool to process multiple sequene alignments and reduce
the number of outlier sequences and artifacts caused by them. The script integrates
EvalMSA and TrimAl, and requires only a FASTA or PHYLIP file as input, although the
user can also choose which normalized weight threshold to use by EvalMSA (default: 0.7) and
if or not want to use trimAl (default: yes). 

## Setting up!
```
git clone https://github.com/biopro/clean-alignment
cd clean-alignment
bash build.sh
chmod +x clean-alignment.py
echo 'PATH=$PATH:'$(pwd) >> ~/.bashrc
bash
```
## Running

### Default settings

```
clean-alignment.py -i my_alignment.fasta \
                   -o my_alignment.clean.fasta
```

### Custom normalized weight threshold

```
clean-alignment.py -i my_alignment.fasta \
                   -o my_alignment.clean.fasta \
                   -wt 0.8
```


