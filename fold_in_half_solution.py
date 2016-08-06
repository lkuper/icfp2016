#!/usr/bin/env python3

# Usage: fold_in_half_solution.py <problem-file>

import sys
import json
import fractions

from problem_parser import parse

# Like paper_drop_solution but tries folding the paper in half horizontally.

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
"""6
0,0
1,0
1,1
0,1
0,1/2
1,1/2
2
4 0 1 5 4
4 2 3 4 5
"""
    ## bottom left corner: stay put
    out += "{0},{1}\n".format(str(lowest_x), str(lowest_y))

    ## bottom right corner: stay put
    out += "{0},{1}\n".format(str(lowest_x+1), str(lowest_y))

    ## top right corner goes to bottom right corner
    out += "{0},{1}\n".format(str(lowest_x+1), str(lowest_y))

    ## top left corner goes to bottom left corner
    out += "{0},{1}\n".format(str(lowest_x), str(lowest_y))

    ## middle of left side stays put
    halfway_left_x = lowest_x
    halfway_left_y = fractions.Fraction(lowest_y + lowest_y+1, 2)

    ## middle of right side stays put
    halfway_right_x = lowest_x + 1
    halfway_right_y = fractions.Fraction(lowest_y + lowest_y+1, 2)

    out += "{0},{1}\n".format(str(halfway_left_x), str(halfway_left_y))
    out += "{0},{1}\n".format(str(halfway_right_x), str(halfway_right_y))
    return out

def main():
    fn = sys.argv[1]
    polygons = parse(fn)

    lowest_x, lowest_y = find_bottom_left(polygons)
    print(paper_drop(lowest_x, lowest_y))

if __name__ == "__main__":
    main()
