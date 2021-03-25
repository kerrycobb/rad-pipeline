#!/usr/bin/env fish

set sampleDir $argv[1]
set outDir $argv[2]
set popMap $argv[3]
set ustacksDir "$outDir"/ustacks

if test -d $ustacksDir
  exit
else
  mkdir $ustacksDir
end

while read line
  set inc (math $inc + 1)
  set filePrefix (string split \t $line)[1]
  set file $sampleDir$filePrefix.1.fq.gz
  echo "module load stacks; ustacks -f $file -o $ustacksDir -i $inc -M 8 -p 1" | myqsub -N ustacks-$filePrefix -d . -j oe -o $ustacksDir 
end < $popMap
