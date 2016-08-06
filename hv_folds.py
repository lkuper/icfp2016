#!/usr/bin/env python3

import sys
from collections import namedtuple
from fractions import Fraction

from problem_parser import parse

## NB: vfolds reduce width.
## (they are like vsplits in vim)
## ALSO NB: hfolds reduce height.

## parts of a solution
## - source point locations
## - facets
## - target locations

## Every point has a source and target location.

def count_folds(width, height):
    """Given a bounding box of w, h, return the number of vfolds and hfolds to
    contain that."""
    return 2, 2


## each of source and dest is an x,y coordinate. Always use fractions.
## TYPE SAFETY AHOY.
SolutionPoint = namedtuple("SolutionPoint", ["source", "dest"])

def solution_for(vfolds, hfolds):
    """Create a Solution for if we want to fold horizontally hfolds times and
    vertically vfolds times."""

    ncolumns = (2 ** vfolds) 
    nrows = (2 ** hfolds) 

    ## How many points?
    npoints = ((2 ** hfolds) + 1) * ((2 ** vfolds) + 1)

    ## how many facets?
    nfacets = ncolumns * nrows

    # print("this many facets & points", nfacets, npoints)

    solution_points = []

    ## For each point, find its source location.
    x_denominator = ncolumns
    y_denominator = nrows
    for y_numerator in range(nrows + 1):
        for x_numerator in range(ncolumns + 1):

            solution_points.append(
                SolutionPoint(
                    # source coords
                    (Fraction(x_numerator, x_denominator),
                     Fraction(y_numerator, y_denominator)),
                    # destination coords
                    (Fraction(x_numerator % 2, x_denominator),
                     Fraction(y_numerator % 2, y_denominator))))

    solution_facets = []
    ## for every point, add a facet unless you're on the right edge or on the
    ## top edge.
    for index, point in enumerate(solution_points):
        right_edge = (point.source[0] == 1)
        top_edge = (point.source[1] == 1)
        if (right_edge or top_edge): continue

        ## Don't stop 'til you get enough.
        if len(solution_facets) == nfacets: break

        solution_facets.append((index, index+1,
                                index + ncolumns + 1 + 1, index + ncolumns + 1))

    return solution_points, solution_facets

def format_solution(soln):
    solution_points, solution_facets = soln
    solution = ""

    # number of source points
    solution += str(len(solution_points)) + "\n"

    # coords of source points
    source_coords = ["{},{}".format(str(point.source[0]), str(point.source[1])) for point in solution_points]
    solution += "\n".join(source_coords)

    # number of facets
    solution += str(len(solution_facets)) + "\n"

    # list of facets w/ vertex indices
    facets = ["{} {}".format(len(facet)," ".join([str(index) for index in facet])) for facet in solution_facets]
    solution += "\n".join(facets)

    # coords of dest points by index
    dest_coords = ["{},{}".format(str(point.dest[0]), str(point.dest[1])) for point in solution_points]
    solution += "\n".join(dest_coords)

    # make sure we have the right number of dest point locations
    assert len(set(dest_coords)) == 4

    print(solution)

def find_bottom_left(polygons):
    lowest_x = float('inf')
    lowest_y = float('inf')

    for key, points in polygons.items():
        for point in points:
            lowest_x = min(point[0], lowest_x)
            lowest_y = min(point[1], lowest_y)
    return (lowest_x, lowest_y)

def find_top_right(polygons):
    highest_x = float('-inf')
    highest_y = float('-inf')

    for key, points in polygons.items():
        for point in points:
            highest_x = max(point[0], highest_x)
            highest_y = max(point[1], highest_y)
    return (highest_x, highest_y)

def smallest_half_bigger_than(num):
    """Returns the smallest number that's >= num that we can achieve by
    repeated halving, or if num is >1, then return 1. Also return how many folds
    we need to get that size"""
    assert num > 0
    cur = Fraction(1, 1)
    nfolds = 0
    while True:
        thenext = Fraction(1, cur.denominator * 2)
        if thenext >= num:
            cur = thenext
            nfolds += 1
        else:
            return cur, nfolds

def main():
    fn = sys.argv[1]
    polygons = parse(fn)

    lowest_x, lowest_y = find_bottom_left(polygons)
    highest_x, highest_y = find_top_right(polygons)

    height = highest_y - lowest_y
    width = highest_x - lowest_x

    print("need to generate a square that covers", lowest_x, lowest_y,
          highest_x, highest_y)

    print(smallest_half_bigger_than(1))
    print(smallest_half_bigger_than(Fraction(1, 2)))
    print(smallest_half_bigger_than(Fraction(1, 3)))
    print(smallest_half_bigger_than(Fraction(1, 15)))
    print(smallest_half_bigger_than(Fraction(1, 16)))

if __name__ == "__main__":
    main()
