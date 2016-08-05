#!/bin/bash

## Download all problems. Turn them all into json. OH YEAH.

python3 download_problems.py

for problem in problems/*; do
  ./parse_problem $problem > "$problem".json
done
