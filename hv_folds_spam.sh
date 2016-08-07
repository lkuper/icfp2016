#!/bin/bash

for i in `seq 7000 1`; do
  problemfile="problems/problem_$(printf "%03d\n" $i)"

  if [ ! -e $problemfile ]; then
    continue
  fi
  echo "doing $i"

  python3 hv_folds.py $problemfile \
  > /tmp/hvfoldssolution
  ./submit_solution $i /tmp/hvfoldssolution
  sleep 3.6s
done
