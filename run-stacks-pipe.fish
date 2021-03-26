#!/usr/bin/env fish

set inDir $argv[1]
set popMap $argv[2]
set n $argv[3]

set outDir $inDir/n"$n"

if test -d $outDir
  echo $outDir already exists
else 
  mkdir $outDir
end

# Create string with input file paths
set inFileString
while read line
  set filePrefix (string split \t $line)[1]
  # Append input file path to inFileString
  set -a inFileString "-s $inDir$filePrefix "
end < $popMap

module load stacks
cstacks -o $outDir $inFileString -n $n -p $PBS_NP 
sstacks -P $outDir -M $popMap -p $PBS_NP
tsv2bam -P $outDir -M $popMap -t $PBS_NP
gstacks -P $outDir -M $popMap -t $PBS_NP 

