
Scripts to facilitate processing of 3RAD data with STACKs.

# Demultiplexing
## 1. Demultiplex iTru7 indexes
Prepare a tab delimited barcodes file with 8 bp index sequence in the first column and ID in the second column. 
Run the `process_radtags_i7.sh` script.
```
process_radtags_i7.sh \
  <path to read 1 sequences> \
  <path to read 2 sequences> \
  <path to barcodes file> \
  <desired output directory path> # Cannot already exist
```

## 2. Declone
Run `clone_filter.py` script.
```
clone_filter.py \
  <path to process_radtags output director> \
  <desired output directory path> # Cannot already exist
```

## 3. Concatenate
Concatenate output from the clone_filter.py script sharing 3RAD adapter indexes (i.e. contains samples from the same project).
#### Example:
```
cat <i7-index1_R1.fq.gz> <i7_index2_R2.fq.gz> ... project1_R1.fq.gz
cat <i7-index1_R1.fq.gz> <i7_index2_R2.fq.gz> ... project1_R2.fq.gz
```

## 4. Demultiplex samples with 3RAD adapter indexes
Prepare a barcodes file with the index sequences of the 3RAD adapters and the corresponding sample IDs. 
A script to facilitate the generation of a barcodes file can be found at <https://github.com/kerrycobb/radseq-barcodes-file-gen>

Run `process_radtags_samples.sh`
```
process_radtags_samples.sh \
  <path to concatenated read 1 reads> \
  <path to concatenated read 2 reads> \
  <path to barcodes file> \
  <desired output directory path> \ # Cannot already exist
  <enzyme 1> \
  <enzyme 2> 

# Stacks Alignment
## Run ustacks
You will need to modify this script to work with your own HPC system.
`run_ustacks.sh <demultiplexed sample directory> <output directory> <populations file>`
