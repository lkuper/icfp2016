#!/bin/bash

for i in `seq 1 5000`; do
  problemfile="problems/problem_$(printf "%03d\n" $i)"

  if [ ! -e $problemfile ]; then
    continue
  fi
  echo "doing $i"

  python3 hv_folds.py $problemfile \
  > /tmp/hvfoldssolution
  ./submit_solution $i /tmp/hvfoldssolution
  sleep 1.5s
done
