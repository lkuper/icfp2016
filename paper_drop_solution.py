#!/usr/bin/env python3

# Usage: paper_drop_solution.py <problem-file>

import sys
import json
import fractions

from problem_parser import parse

def find_bottom_left(polygons):
    lowest_x = float('inf')
    lowest_y = float('inf')

    for key, points in polygons.items():
        for point in points:
            lowest_x = min(point[0], lowest_x)
            lowest_y = min(point[1], lowest_y)
    return (lowest_x, lowest_y)

def paper_drop(lowest_x, lowest_y):
    out = \
"""4
0,0
1,0
1,1
0,1
1
4 0 1 2 3
"""
    out += "{0},{1}\n".format(str(lowest_x), str(lowest_y))
    out += "{0},{1}\n".format(str(lowest_x+1), str(lowest_y))
    out += "{0},{1}\n".format(str(lowest_x+1), str(lowest_y+1))
    out += "{0},{1}\n".format(str(lowest_x), str(lowest_y+1))
    return out

def main():
    fn = sys.argv[1]
    polygons = parse(fn)

    lowest_x, lowest_y = find_bottom_left(polygons)
    print(paper_drop(lowest_x, lowest_y))

if __name__ == "__main__":
    main()
