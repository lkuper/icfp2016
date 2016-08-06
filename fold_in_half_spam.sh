#!/bin/bash

for i in `seq 1 101`; do
  python3 fold_in_half_solution.py problems/problem_$(printf "%03d\n" $i) \
  > /tmp/foldinhalfsolution
  ./submit_solution $i /tmp/foldinhalfsolution
  sleep 1.5s
done
