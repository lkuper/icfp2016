#!/usr/bin/env python3

# Usage: fold_in_half_solution.py <problem-file>

import sys
import json
import fractions

# Like paper_drop_solution but tries folding the paper in half horizontally.

def convert_coord(coord):
    if "/" in coord:
        parts = coord.split("/")
        num = fractions.Fraction(int(parts[0]), int(parts[1]))
    else:
        num = fractions.Fraction(int(coord), 1)
    return num

def parse(fn):
    with open(fn) as f:
        lines = f.readlines()
    
    polygons = {}
    num_polygons = 0
    vertex_counts = [] # list of lists of vertices
    lines = [x.strip('\n') for x in lines]

    num_polygons = int(lines[0])
    cur_polygon = 0
    cur_vertex = 0

    # First line is the number of polygons we're expecting, so skip it
    for line in lines[1:]:
    
        # If there's no comma, we've got a new polygon
        if "," not in line:
            cur_polygon = cur_polygon + 1

            # if we've gotten through all the polygons, we're done!
            if cur_polygon > num_polygons:
                break

            # reset number of vertices
            cur_vertex = 0
            polygons[cur_polygon] = []
        
        # If there's a comma, we've got a new vertex
        elif "," in line:
            coords = line.split(",")
            cur_vertex = cur_vertex + 1
            coords = [convert_coord(coord) for coord in coords]

            polygons[cur_polygon].append(coords)
    return polygons

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
