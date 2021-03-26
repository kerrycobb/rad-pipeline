#!/usr/bin/env bash

READ1=$1
READ2=$2
OUTDIR=$3

module load stacks 
clone_filter \
  -1 $READ1 \
  -2 $READ2 \
  -o $OUTDIR \
  -i gzfastq \
  --null_index \
  --oligo_len_2 8