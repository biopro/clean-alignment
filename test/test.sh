#!/usr/bin/env bash

cd test
python ../clean-alignment.py -i ../test/sequences.fasta \
       -if fasta -o alignment.clean.fasta -of fasta 
