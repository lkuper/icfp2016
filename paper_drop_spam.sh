#!/bin/bash

for i in `seq 1 101`; do
  python3 paper_drop_solution.py problems/problem_$(printf "%03d\n" $i) \
  > /tmp/paperdropsolution
  ./submit_solution $i /tmp/paperdropsolution
  sleep 1.5s
done
