#!/usr/bin/env fish

set inDir $argv[1]

set incomp 0
for i in "$inDir"/ustacks-*                                                              
  set end (tail -1 $i)
  if [ $end != "ustacks is done." ]
    echo $i not complete
    set (math $incomp += 1)
  end
end

if [ $incomp -eq 0 ]
  echo All runs completed!
end


