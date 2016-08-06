#!/bin/bash

## Download all problems. Turn them all into json. OH YEAH.

python3 download_problems.py

rm problems/*.json

for problem in problems/*; do
  echo $problem;
  ./parse_problem $problem > "$problem".json
done
