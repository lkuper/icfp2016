#!/bin/bash

# 6258 is the largest problem ID on the postmortem server.
for i in `seq 1 6258`; do
  problemfile="problems/problem_$(printf "%04d\n" $i)"

  if [ ! -e $problemfile ]; then
    continue
  fi
  echo "doing $i"

  python3 paper_drop_solution.py $problemfile \
  > /tmp/paperdropsolution
  ./submit_solution.sh $i /tmp/paperdropsolution
  # We can make one API request every 3.6 seconds indefinitely without
  # running out of API requests.
  sleep 3.6s
done
