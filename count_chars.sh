#!/bin/bash

# Usage: count_chars.sh <filename>

tr -d '[:space:] ' <  $1 | wc -c
