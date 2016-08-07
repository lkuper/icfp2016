# based on Active State Recipe 117225 by David Eppstein

import sys
from problem_parser import parse

def orientation(p, q, r):
    '''Return positive if p-q-r are clockwise, neg if ccw, zero if colinear.'''
    return (q[1]-p[1])*(r[0]-p[0]) - (q[0]-p[0])*(r[1]-p[1])

def hulls(Points):
    U = []
    L = []
    Points.sort()
    for p in Points:
        while len(U) > 1 and orientation(U[-2],U[-1],p) <= 0: U.pop()
        while len(L) > 1 and orientation(L[-2],L[-1],p) >= 0: L.pop()
        U.append(p)
        L.append(p)
    return U,L

def rotatingCalipers(Points):
    '''Given a list of 2d points, finds all ways of sandwiching the points
between two parallel lines that touch one point each, and yields the sequence
of pairs of points touched by each pair of lines.'''
    U,L = hulls(Points)
    i = 0
    j = len(L) - 1
    while i < len(U) - 1 or j > 0:
        yield U[i],L[j]
        
        # if all the way through one side of hull, advance the other side
        if i == len(U) - 1: j -= 1
        elif j == 0: i += 1
        
        # still points left on both lists, compare slopes of next hull edges
        # being careful to avoid divide-by-zero in slope calculation
        elif (U[i+1][1]-U[i][1])*(L[j][0]-L[j-1][0]) > \
                (L[j][1]-L[j-1][1])*(U[i+1][0]-U[i][0]):
            i += 1
        else: j -= 1

def diameter(Points):
    '''Given a list of 2d points, returns the pair that's farthest apart.'''
    themax = 0
    out = None
    for p,q in rotatingCalipers(Points):
        diam = (p[0]-q[0])**2 + (p[1]-q[1])**2
        if diam >= themax:
            themax = diam
            out = (p,q)
    return out

def list_all_angles(polygons):
    """Returns set of all the rise/run ratios that occur in the polygons."""
    out = set()
    for key, points in polygons.items():
        point = None
        firstpoint = points[0]
        prevpoint = points[0]
        for point in points[1:]:
            xdiff = point[0] - prevpoint[0]
            ydiff = point[1] - prevpoint[1]
            if xdiff == 0:
                out.add(float('inf'))
            else:
                out.add(ydiff / xdiff)
            prevpoint = point
        ## and back to the beginning
        xdiff = firstpoint[0] - prevpoint[0]
        ydiff = firstpoint[1] - prevpoint[1]
        if xdiff == 0:
            out.add(float('inf') * ydiff)
        else:
            out.add(ydiff / xdiff)
    return out

def list_destination_points(polygons):
    out = []
    for key, points in polygons.items():
        for point in points:
            out.append(point)
    return out

def diameter_tangent(polygons):
    """Get the rise/run for the diameter of this set of polygons."""
    points = list_destination_points(polygons)
    p1, p2 = diameter(points)

    xdiff = p1[0] - p2[0]
    ydiff = p1[1] - p2[1]
    return float('inf') if (xdiff == 0) else (ydiff / xdiff)

def best_angle(polygons):
    """Find the angle present in the polygons most like the angle of its
    diameter."""
    tangents = list_all_angles(polygons)
    dtan = diameter_tangent(polygons)

    if dtan == float('inf'):
        dtan = sys.maxsize

    smallest_diff = float('inf')
    best_tan = None
    for tan in tangents:
        thediff = abs(dtan - tan)
        if thediff < smallest_diff:
            best_tan = tan
            smallest_diff = abs(dtan - tan)
    return best_tan

def main():
    ## points = [(0,0), (2, 2), (1,0), (1,72), (0,1)]
    fn = sys.argv[1]
    problem = parse(fn)
    points = list_destination_points(problem)
    print(best_angle(problem))

if __name__ == "__main__": main()
