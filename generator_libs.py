#!/usr/bin/python3
import math
# These are helper functions for use in pattern generators.
from constants import *
def distance(x, y):
    return math.sqrt(x*x + y*y)

def lawOfCosines(a, b, c):
    return math.acos((a*a + b*b - c*c) / (2 * a * b))

def cartesian_calc(x, y):
    # Mostly stolen directly from https://appliedgo.net/roboticarm/
    # This calculates the angles for the steppers and calls returns the two angles.
    dist = distance(x, y)
    d1 = math.atan2(y,x)
    d2 = lawOfCosines(dist, ARM_1_LENGTH, ARM_2_LENGTH)
    a1 = d1 + d2
    a2 = lawOfCosines(ARM_1_LENGTH, ARM_2_LENGTH, dist)

    # Convert to degrees and map the angle of the first arm onto the second
    a1 = (a1*180)/math.pi
    a2 = (a2*180)/math.pi+(a1-180)

    # Due to dark geomancies these two angles are interchangable - they both result
    # in the same end point.
    return (a1%360, a2%360)


def wrapping_diff(x, y):
    diff = x - y
    return (diff + 180) % 360 - 180

# Mostly stolen directly from https://stackoverflow.com/questions/1119627/how-to-test-if-a-point-is-inside-of-a-convex-polygon-in-2d-integer-coordinates
def inside_convex_polygon(point, vertices):
    previous_side = None
    n_vertices = len(vertices)
    for n in range(n_vertices):
        a, b = vertices[n], vertices[(n+1)%n_vertices]
        affine_segment = v_sub(b, a)
        affine_point = v_sub(point, a)
        current_side = get_side(affine_segment, affine_point)
        if current_side is None:
            return False #outside or over an edge
        elif previous_side is None: #first segment
            previous_side = current_side
        elif previous_side != current_side:
            return False
    return True

RIGHT = "RIGHT"
LEFT = "LEFT"
def get_side(a, b):
    x = cosine_sign(a, b)
    if x < 0:
        return LEFT
    elif x > 0:
        return RIGHT
    else:
        return None

def v_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def cosine_sign(a, b):
    return a[0]*b[1]-a[1]*b[0]

def sum_distance_p_a_p_b(p, a, b):
    return distance(p[0]-a[0], p[1]-a[1]) + distance(p[0]-b[0], p[1]-b[1])

def filter_coordinate(point, vertices):
    # This function returns a (x,y) tuple after it's been bounds-capped to fit inside the enclosure.
    if inside_convex_polygon(point, vertices):
        return point
    # Now we need to limit the coordinate to the edge of the enclosure
    n_vertices = len(vertices)
    min_distance = -1
    closest_vertices = [vertices[0], vertices[1]]
    for n in range(n_vertices):
        a, b = vertices[n], vertices[(n+1)%n_vertices]
        d = sum_distance_p_a_p_b(point, a, b)
        if min_distance == -1 or min_distance > d:
            min_distance = d
            closest_vertices = [a,b]
    # For less mess
    a, b = closest_vertices
    p = point
    v_a_p = (p[0]-a[0], p[1]-a[1])
    v_a_b = (b[0]-a[0], b[1]-a[1])
    smag_a_b = v_a_b[0]**2 + v_a_b[1]**2
    ABAPproduct = v_a_b[0]*v_a_p[0] + v_a_b[1]*v_a_p[1]
    # Listen: I'm just as much at sea as you. I'm just copying this from someone convincing on stackoverflow:
    # https://stackoverflow.com/questions/3120357/get-closest-point-to-a-line
    dist = ABAPproduct / smag_a_b
    if dist < 0:
        return a
    elif dist > 1:
        return b
    else:
        return (a[0]+v_a_b[0]*dist, a[1]+v_a_b[1]*dist)

class vector2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def set_zero(self):
        self.x = 0
        self.y = 0
    def copy(self, p):
        self.x = p.x
        self.y = p.y
    def vector_to(self, p):
        return self.__sub__(p)
    def distance_to(self, p):
        return distance(p.x-self.x, p.y-self.y)
    def magnitude(self):
        return distance(self.x, self.y)
    def set_magnitude(self, m):
        scale = m/self.magnitude()
        self.x *= scale
        self.y *= scale
    def cap_magnitude(self, m):
        if self.magnitude() > m:
            self.set_magnitude(m)
    def rotate(self, degrees):
        rad = math.radians(degrees)
        x_temp = self.x
        y_temp = self.y
        self.x = x_temp*math.cos(rad)-y_temp*math.sin(rad)
        self.y = x_temp*math.sin(rad)+y_temp*math.cos(rad)
        return self
    def __add__(self, p):
        return vector2(p.x+self.x, p.y+self.y)
    def __sub__(self, p):
        return vector2(p.x-self.x, p.y-self.y)
    def __eq__(self, p):
        return p.x==self.x and p.y==self.y
    def __ne__(self, p):
        return not self.__eq__(p)
    def __str__(self):
        return "({},{})".format(self.x, self.y)
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise ValueError()
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise ValueError()


HOME_X = "G28 X"
HOME_Y = "G28 Y"
XY = "G1 X{} Y{}"
EDGE_R=175

def circle_points(r, n):
    for i in range(n):
        angle = math.radians(i*(360/n))
        x = math.trunc(r*math.sin(angle))
        y = math.trunc(r*math.cos(angle))
        yield vector2(x, y)

def g(p):
    # Returns a G1 command for that point
    return XY.format(p.x, p.y)
