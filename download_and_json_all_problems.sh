#!/bin/bash

## Download all problems. Turn them all into json. OH YEAH.

python3 download_problems.py

rm problems/*.json

for problem in problems/*; do
  echo $problem;
  python3 parse_problem.py $problem > "$problem".json
done
