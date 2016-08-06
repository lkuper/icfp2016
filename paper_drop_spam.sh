#!/bin/bash

for i in `seq 1 5000`; do
  problemfile="problems/problem_$(printf "%03d\n" $i)"

  if [ ! -e $problemfile ]; then
    continue
  fi
  echo "doing $i"

  python3 paper_drop_solution.py $problemfile \
  > /tmp/paperdropsolution
  ./submit_solution $i /tmp/paperdropsolution
  sleep 1.5s
done
