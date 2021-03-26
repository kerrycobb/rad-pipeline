#!/usr/bin/env fish

# 

set sampleDir $argv[1]
set outDir $argv[2]
set popMap $argv[3]
set M $argv[4]

set ustacksDir "$outDir"/M"$M"/ustacks

if test -d $ustacksDir
  $ustacksDir already exists
  exit
else
  mkdir $ustacksDir
end

while read line
  set inc (math $inc + 1)
  set filePrefix (string split \t $line)[1]
  set file $sampleDir$filePrefix.1.fq.gz
  echo "module load stacks; ustacks -f $file -o $ustacksDir -i $inc --name $filePrefix -M $M -p 1" | myqsub --time 4:00:00 --mem 5gb -N ustacks-$filePrefix -d . -j oe -o $ustacksDir 
end < $popMap
