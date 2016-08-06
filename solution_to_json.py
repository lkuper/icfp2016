#!/usr/bin/env python3

## For right now, just get out the set of destination points as a json list.
## Output should be like [[x1, y1], [x2, y2], ...]

# Usage: python3 solution_to_json.py solution_file (otherwise read from stdin)

import fileinput
import json

def convert_coord(coord):
    if "/" in coord:
        parts = coord.split("/")
        num = float(parts[0]) / float(parts[1])
    else:
        num = float(coord)
    return num

def main():
    dest_points = []

    lines = []
    for line in fileinput.input():
        lines.append(line.strip())
    
    lineptr = 0
    num_source_points = int(lines[lineptr])
    lineptr += 1

    for i in range(num_source_points):
        lineptr += 1

    num_facets = int(lines[lineptr])
    lineptr += 1
    for i in range(num_facets):
        lineptr += 1

    for line in lines[lineptr:]:
        assert "," in line
        x, y = [convert_coord(s) for s in line.split(",")]
        dest_points.append((x,y))
        
    json_solution = json.dumps(dest_points)
    print(json_solution)

if __name__ == "__main__":
    main()
