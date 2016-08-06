import fractions

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
