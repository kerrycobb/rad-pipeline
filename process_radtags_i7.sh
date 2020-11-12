#!/usr/bin/env bash

READ1=$1
READ2=$2
BARCODES=config/barcodes-i7.tsv
OUTDIR=output/process-radtags-i7/

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
    -i gzfastq \
    --barcode_dist_1 1 \
    --rescue \
    --index_null \
    --disable_rad_check \
    --retain_header