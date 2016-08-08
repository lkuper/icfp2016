#!/bin/bash

# 6258 is the largest problem ID on the postmortem server.
for i in `seq 1 6258`; do
  problemfile="problems/problem_$(printf "%04d\n" $i)"

  if [ ! -e $problemfile ]; then
    continue
  fi
  echo "doing $i"

  python3 fold_in_half_solution.py $problemfile \
  > /tmp/foldinhalfsolution
  ./submit_solution.sh $i /tmp/foldinhalfsolution
  # We can make one API request every 3.6 seconds indefinitely without
  # running out of API requests.
  sleep 3.6s
done
