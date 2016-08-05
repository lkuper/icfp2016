#! /usr/bin/env python3

# Usage: parse-problem <problem-file>

import sys
import json

def convert_coord(coord):
    if "/" in coord:
        parts = coord.split("/")
        num = float(parts[0]) / float(parts[1])
    else:
        num = float(coord)
    return num

def main():
    filename = sys.argv[1]

    problem = {}
    problem["skeleton"] = []

    num_polygons = 0
    vertex_counts = [] # list of lists of vertices

    with open(filename) as f:
        lines = f.readlines()
    
    lines = [x.strip('\n') for x in lines]

    num_polygons = int(lines[0])
    cur_polygon = 0
    cur_vertex = 0

    # First line is the number of polygons we're expecting, so skip it
    for line in lines[1:]:
    
        # If there's no comma, we've got a new polygon
        if "," not in line:
            cur_polygon = cur_polygon + 1

            # if we've gotten through all the polygons, it's time to
            # parse the skeleton
            if cur_polygon > num_polygons:
                continue;

            # reset number of vertices
            cur_vertex = 0
            problem[cur_polygon] = []
        
        # If there's a comma and we're not done parsing polygons yet,
        # we've got a new vertex
        elif "," in line and cur_polygon <= num_polygons:
            coords = line.split(",")
            cur_vertex = cur_vertex + 1
            #print("vertex", cur_vertex, "of polygon", cur_polygon, "is", coords)

            # Divide out fractions; convert to floats
            coords = [convert_coord(coord) for coord in coords]

            problem[cur_polygon].append(coords)

        # If there's a comma and we're done parsing polygons,
        # we've got a skeleton segment
        elif "," in line and cur_polygon > num_polygons:
            endpoints = line.split(" ")
            endpoints = [endpoint.split(",") for endpoint in endpoints]
            endpoints = [[convert_coord(coord) for coord in endpoint] for endpoint in endpoints]
            problem["skeleton"].append(endpoints)

    json_problem = json.dumps(problem)

    print(json_problem)

if __name__ == "__main__":
    main()
