#!/usr/bin/env python3

import sys
import copy
from collections import namedtuple
from fractions import Fraction
import math

from problem_parser import parse
import calipers

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


def irregular_fold(left_fold_length, down_fold_length):
    """Create a Solution for if we want to fold over toward the left
    left_fold_length, and toward down from the top down_fold_length."""

    #print(left_fold_length, down_fold_length)

    # Only works for folds that are less than half the paper width.
    assert left_fold_length < 0.5
    assert down_fold_length < 0.5

    solution_points = []

    # print("left_fold_length", left_fold_length)
    # print("down_fold_length", down_fold_length)

    remaining_width = 1 - (left_fold_length * 2)
    remaining_height = 1 - (down_fold_length * 2)

    ## left to right
    col_widths       = [1 - left_fold_length, left_fold_length]
    x_source_offsets = [sum(col_widths[0:i]) for i in range(0, 3)]
    x_dest_offsets   = [0, 1 - left_fold_length, remaining_width]

    ## bottom to top
    row_heights      = [1 - down_fold_length, down_fold_length]
    y_source_offsets = [sum(row_heights[0:i]) for i in range(0, 3)]
    y_dest_offsets   = [0, 1 - down_fold_length, remaining_height]

    for y in range(0, 3):
        for x in range(0, 3):
            solution_points.append(
                SolutionPoint(
                    # source coords
                    (Fraction(x_source_offsets[x]),
                     Fraction(y_source_offsets[y])),
                    # destination coords
                    (Fraction(x_dest_offsets[x]),
                     Fraction(y_dest_offsets[y]))))

    solution_facets = [(0, 1, 4, 3),
                       (1, 2, 5, 4),
                       (4, 5, 8, 7),
                       (3, 4, 7, 6)]
    return solution_points, solution_facets

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

    ## Source and destination coords for every point.
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
    solution += "\n".join(source_coords) + "\n"

    # number of facets
    solution += str(len(solution_facets)) + "\n"

    # list of facets w/ vertex indices
    facets = ["{} {}".format(len(facet)," ".join([str(index) for index in facet])) for facet in solution_facets]
    solution += "\n".join(facets) + "\n"

    # coords of dest points by index
    dest_coords = ["{},{}".format(str(point.dest[0]), str(point.dest[1])) for point in solution_points]
    solution += "\n".join(dest_coords) + "\n"

    # make sure we have the right number of dest point locations
    # assert len(set(dest_coords)) == 4

    return solution

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
    we need to get that size."""
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

def offset_solution_by(soln, offset_x, offset_y):
    """Make a new solution in which all destination coordinates have been
    shifted by the given offset."""
    points, facets = soln
    outpoints = []
    for point in points:
        outpoints.append(SolutionPoint(point.source,
                                       # destination coords
                                       ((point.dest[0] + offset_x),
                                        (point.dest[1] + offset_y))))
    return (outpoints, facets)

def rotate_solution(soln, theta):
    points, facets = soln
    destpoints = [(point.dest[0], point.dest[1]) for point in points]
    rotated_destpoints = rotate_polygon(destpoints, theta)
    fractified = [(Fraction(point[0]), Fraction(point[1])) for point in rotated_destpoints]

    assert len(points) == len(fractified)

    outpoints = []
    for i in range(0, len(points)):
        outpoints.append(SolutionPoint(points[i].source,
                                       # destination coords
                                       fractified[i]))
    return outpoints, facets

## NB: this one does offsetting too.
def rotate_solution_by(soln, theta, problem_polygons):
    points, facets = soln

    destpoints = [(point.dest[0], point.dest[1]) for point in points]
    rotated_destpoints = rotate_polygon(destpoints, theta)
    fractified = [(Fraction(point[0]), Fraction(point[1])) for point in rotated_destpoints]

    assert len(points) == len(fractified)

    outpoints = []
    for i in range(0, len(points)):
        outpoints.append(SolutionPoint(points[i].source,
                                       # destination coords
                                       fractified[i]))
    # Last step: offset.
    problem_leftmost = float('inf')
    for key, points in problem_polygons.items():
        for point in points:
            problem_leftmost = min(point[0], problem_leftmost)

    problem_bottommost = float('inf')
    for key, points in problem_polygons.items():
        for point in points:
            problem_bottommost = min(point[1], problem_bottommost)

    soln_leftmost = float('inf')
    for point in fractified:
        soln_leftmost = min(point[0], soln_leftmost)

    soln_bottommost = float('inf')
    for point in fractified:
        soln_bottommost = min(point[1], soln_bottommost)

    offset_x = problem_leftmost - soln_leftmost
    offset_y = problem_bottommost - soln_bottommost

    soln = offset_solution_by((outpoints, facets), offset_x, offset_y)

    return soln


# Adapted from http://stackoverflow.com/questions/20023209/python-function-for-rotating-2d-objects
def rotate_polygon(polygon, theta):
    """Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = math.radians(theta) # convert degrees to radians
    rotated_polygon = []
    for corner in polygon:
        rotated_polygon.append(
            (Fraction(corner[0]*math.cos(theta)-corner[1]*math.sin(theta)),
             Fraction(corner[0]*math.sin(theta)+corner[1]*math.cos(theta)))
        )

    return rotated_polygon

def quantize_solution(soln, max_denominator):
    points, facets = soln
    outpoints = []
    for point in points:
        outpoints.append(SolutionPoint(point.source,
                                       # destination coords
                                       ((point.dest[0].limit_denominator(max_denominator)),
                                        (point.dest[1].limit_denominator(max_denominator)))))
    return (outpoints, facets)

def rectified_box_resemblance(bounding1, bounding2):
    """Given two width,height tuples, calculate the resemblance score for those
    two boxes."""
    ## computing the intersection
    right = min(bounding1[0], bounding2[0])
    top = min(bounding1[1], bounding2[1])

    intersection = right * top
    ## computing the overlap area
    overlap = (bounding1[0] * bounding1[1] +
               bounding2[0] * bounding2[1] -
               intersection)
    return intersection / overlap

## what's the best you can do with irregular?
def best_irregular_resemblance(probwidth, probheight):
    """Return resemblance score that we *could* get for a given width and
    height. Also return left fold length and down fold length."""
    ourwidth = min(Fraction(99,100), max(Fraction(51,100), probwidth))
    ourheight = min(Fraction(99,100), max(Fraction(51,100), probheight))
    ourscore = rectified_box_resemblance((probwidth, probheight),
                                         (ourwidth, ourheight))
    return ourscore,(1-ourwidth,1-ourheight)

def best_regular_resemblance(probwidth, probheight):
    """Return resemblance score that we *could* get for a given width and
    height. Also returns the (vfolds, hfolds) tuple."""

    ourwidth, vfolds = smallest_half_bigger_than(probwidth)
    ourheight, hfolds = smallest_half_bigger_than(probheight)

    smaller_width = ourwidth / 2
    more_vfolds = vfolds + 1
    smaller_height = ourheight / 2
    more_hfolds = hfolds + 1

    ourboxes = []
    ## small small
    ourboxes.append((smaller_width, smaller_height))
    ## small big
    ourboxes.append((smaller_width, ourheight))
    ## big small
    ourboxes.append((ourwidth, smaller_height))
    ## big big
    ourboxes.append((ourwidth, ourheight))

    scores_indices = [(rectified_box_resemblance((probwidth, probheight),
                                                  bounding),
                       i)
                      for i,bounding in enumerate(ourboxes)]
    maxscore,maxindex = max(scores_indices)

    ## ... could have done this cleaner.
    if maxindex == 0:
        return maxscore, (more_vfolds, more_hfolds)
    elif maxindex == 1:
        return maxscore, (more_vfolds, hfolds)
    elif maxindex == 2:
        return maxscore, (vfolds, more_hfolds)
    elif maxindex == 3:
        return maxscore, (vfolds, hfolds)
    else:
        assert False, "something is very wrong"

def solve_simple_case(polygons):
    lowest_x, lowest_y = find_bottom_left(polygons)
    highest_x, highest_y = find_top_right(polygons)

    ## bounding box of the problem.
    width = highest_x - lowest_x
    height = highest_y - lowest_y

    regscore,(vfolds,hfolds) = best_regular_resemblance(width, height)
    irregscore,(lfold,dfold) = best_irregular_resemblance(width, height)

    if regscore >= irregscore:
        soln = solution_for(vfolds, hfolds)
    else:
        soln = irregular_fold(lfold, dfold)

    return offset_solution_by(soln, lowest_x, lowest_y)

def main():
    # TODO: figure this out programmatically
    MAX_DENOMINATOR = 100000

    fn = sys.argv[1]
    polygons = parse(fn)

    # Rotation code! And it would have worked, too, if not for you meddling
    # numerical instability. (works sometimes)
    if False:
        best_tan = calipers.best_angle(polygons)
        theta = math.degrees(math.atan(best_tan))

        ## do opposite rotation
        ## It's never too late for Python mastery.
        new_polys = {k: rotate_polygon(polygons[k], -theta)
                     for k in polygons}

        ## get solution
        soln = solve_simple_case(new_polys)

        ## rotate it back.
        soln = rotate_solution(soln, theta)

        # Try to fix numeric instability
        soln = quantize_solution(soln, MAX_DENOMINATOR)
    else:
        ## Boring, non-rotational case.
        soln = solve_simple_case(polygons)

    out = format_solution(soln)
    print(out)

if __name__ == "__main__":
    main()
