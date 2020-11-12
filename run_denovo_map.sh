#!/usr/bin/env bash

SAMPLE_DIR=$1
OUT_DIR=$2
POP_MAP=$3
M=$4
n=$5
MAX_GAPS=$6
ALN_LEN=$7

ALIGN_DIR=$OUT_DIR$(echo M${M}_n${n}_mg${MAX_GAPS}_al${ALN_LEN})
CAT_DIR=$ALIGN_DIR/catalog
ALL_SNP_DIR=$ALIGN_DIR/all-snps_all-loci
# SINGLE_SNP_DIR=$ALIGN_DIR/out_single-snp_all-loci

mkdir -p $ALIGN_DIR
mkdir -p $CAT_DIR
mkdir -p $ALL_SNP_DIR
# mkdir -p $SINGLE_SNP_DIR

# Run stacks pipeline and populations with no filtering and with all sites
module load stacks
denovo_map.pl \
  --samples $SAMPLE_DIR \
  --popmap $POP_MAP \
  --out-path $CAT_DIR \
  -M $M -n $n \
  -T $PBS_NP \
  --paired \
  -X "cstacks:--max-gaps $MAX_GAPS --min-aln-len $ALN_LEN" \
  -X "populations: --out-path $ALL_SNP_DIR --fasta-samples --fasta-loci --structure --phylip-var --phylyp-var-all"

# # mv $CAT_DIR/populations* $ALL_SNP_DIR

# Strip comment line from output
sed -i '/^#/d' $ALL_SNP_DIR/populations.var.phylip
# sed -i '/^#/d' $ALL_SNP_DIR/populations.var.all.phylip




# # Generate fullseq.phy with custom script
# concat-samples-fa \
#   $ALL_SNP_DIR/populations.samples.fa \
#   $ALL_SNP_DIR/populations.fullseq.phy

# # # Run populations sampling only a single snp
# # populations \
# #   -P $CAT_DIR \
# #   -O $SINGLE_SNP_DIR \
# #   -M $POP_MAP \
# #   -t $PBS_NP \
# #   --write_single_snp \
# #   --fasta_loci \
# #   --fasta_samples \
# #   --structure \
# #   --phylip_var
