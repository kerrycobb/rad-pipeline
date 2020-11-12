#!/usr/bin/env bash

READ1=$1
READ2=$2
BARCODES=$3
OUTDIR=$4
ENZYME1=$5
ENZYME2=$6


if [ ! -d $OUTDIR ]
then
    mkdir -p $OUTDIR
else
    echo "$OUTDIR already exists"
    exit 1
fi

module load stacks 
process_radtags \
    -1 $READ1 \
    -2 $READ2 \
    -b $BARCODES \
    -o $OUTDIR \
    --renz_1 $ENZYME1 \
    --renz_2 $ENZYME2 \
    --barcode_dist_1 2 \
    --barcode_dist_2 2 \
    -i gzfastq \
    --rescue \
    --quality \
    --clean \
    --filter_illumina \
    --inline_inline \
    --retain_header
