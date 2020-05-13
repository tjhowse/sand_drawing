# pylint: disable=E0401
from math import acos, atan2, sqrt, pi
from constants import *
try:
    from utime import ticks_us, ticks_diff
except ImportError:
    # This isn't running on-target. We don't need these.
    pass

def distance(x, y):
    return sqrt(x*x + y*y)

def lawOfCosines(a, b, c):
    return acos((a*a + b*b - c*c) / (2 * a * b))

def cartesian_calc(x, y):
    # Mostly stolen directly from https://appliedgo.net/roboticarm/
    # This calculates the angles for the steppers and calls returns the two angles.
    dist = distance(x, y)
    d1 = atan2(y,x)
    d2 = lawOfCosines(dist, ARM_1_LENGTH, ARM_2_LENGTH)
    a1 = d1 + d2
    a2 = lawOfCosines(ARM_1_LENGTH, ARM_2_LENGTH, dist)

    # Convert to degrees and map the angle of the first arm onto the second
    a1 = (a1*180)/pi
    a2 = (a2*180)/pi+(a1-180)

    # Due to dark geomancies these two angles are interchangable - they both result
    # in the same end point.
    return (a1%360, a2%360)

# Mostly stolen directly from https://stackoverflow.com/questions/1119627/how-to-test-if-a-point-is-inside-of-a-convex-polygon-in-2d-integer-coordinates
ARM_1_LENGTH = 100
ARM_2_LENGTH = 100

def wrapping_diff(x, y):
    diff = x - y
    return (diff + 180) % 360 - 180

RIGHT = "RIGHT"
LEFT = "LEFT"

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
    def __add__(self, p):
        return vector2(p.x+self.x, p.y+self.y)
    def __sub__(self, p):
        return vector2(p.x-self.x, p.y-self.y)
    def __eq__(self, p):
        return p.x==self.x and p.y==self.y
    def __ne__(self, p):
        return not self.__eq__(p)


class cnc():
    move_mode = 0
    coord_mode = 0
    debug = True
    gcode = None
    origin = vector2()
    move_vector = vector2()
    intermediate_target = vector2()
    target = vector2()
    arm_1_angle = 0
    arm_2_angle = 0
    pwm_move = False # Movement modes using PWM to drive steppers. Faster, less precise.

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def set_pattern(self, new_pattern):
        print(new_pattern)
        self.pattern = new_pattern
        self.pattern_step = 0
        self.set_gcode(self.pattern[self.pattern_step])

    def set_gcode(self, gcode):
        self.gcode = gcode.split(' ')
        if self.debug:
            print(self.gcode)
        if self.gcode[0] == "G28":
            self.s1.set_speed(0)
            self.s2.set_speed(0)
            if len(self.gcode) == 1:
                return
            if self.gcode[1] == 'Y':
                if self.debug:
                    print("Homing Y axis")
                self.s2.home()
            elif self.gcode[1] == 'X':
                if self.debug:
                    print("Homing X axis")
                self.s1.home()
            return

        elif self.gcode[0] in ["G0", "G1"]:
            self.pwm_move = self.gcode[0] == "G0"
            if len(self.gcode) == 1:
                return
            for coord in self.gcode[1:]:
                if self.coord_mode == 0:
                    if self.move_mode == 0:
                        # Continuous raw movement
                        if coord.startswith('X'):
                            self.s1.set_speed(float(coord[1:]), pwm_motion=self.pwm_move)
                        elif coord.startswith('Y'):
                            self.s2.set_speed(float(coord[1:]), pwm_motion=self.pwm_move)
                    elif self.move_mode == 1:
                        # Discrete raw movement
                        if coord.startswith('X'):
                            self.arm_1_angle = float(coord[1:])
                            self.s1.set_angle(self.arm_1_angle, pwm_motion=self.pwm_move)
                        elif coord.startswith('Y'):
                            self.arm_2_angle = float(coord[1:])
                            self.s2.set_angle(self.arm_2_angle, pwm_motion=self.pwm_move)
                        elif coord.startswith('S'):
                            # This is where the speed of the movement is set.
                            pass
                    elif self.move_mode == 2:
                        # Absolute cartesian positioning
                        if coord.startswith('X'):
                            self.target.x = float(coord[1:])
                        elif coord.startswith('Y'):
                            self.target.y = float(coord[1:])
                        elif coord.startswith('S'):
                            # This is where the speed of the movement is set.
                            pass

            if self.move_mode == 2:
                # TODO translate other movement modes into cartesian points so they can be filtered too.
                if self.debug: print("Unfiltered coordinates: {}".format((self.target.x, self.target.y)))
                (self.target.x, self.target.y) = filter_coordinate((self.target.x, self.target.y), ENCLOSURE_VERTICES)
                if self.debug: print("Filtered coordinates: {}".format((self.target.x, self.target.y)))
                self.move_vector = self.origin.vector_to(self.target)
                move_mag = self.move_vector.magnitude()
                if move_mag > PATH_SPLIT_SIZE:
                    # This move needs to be split up. Create a vector for calculating stepwise
                    # movements along this path
                    points = math.ceil(move_mag/PATH_SPLIT_SIZE)
                    self.move_vector.cap_magnitude(move_mag/points)
            return
        elif self.gcode[0] == "G15":
            # Set coordinate mode
            if len(self.gcode) == 1:
                return
            self.coord_mode = int(self.gcode[1])
            return
        elif self.gcode[0] == "G16":
            # Set movement mode
            if len(self.gcode) == 1:
                return
            self.move_mode = int(self.gcode[1])
            return
        elif self.gcode[0] == "J0":
            # Jump to a line in the gcode pattern
            step = int(self.gcode[1])
            if 0 <= step < len(self.pattern):
                self.pattern_step = step
                self.set_gcode(self.pattern[self.pattern_step])

    def start_move_to_point(self, p):
        self.origin = p
        if (p.x == p.y == 0):
            # Handle the zero case.
            self.arm_2_angle = self.arm_1_angle-180
            self.s1.set_angle(self.arm_1_angle, pwm_motion=self.pwm_move)
            self.s2.set_angle(self.arm_2_angle, pwm_motion=self.pwm_move)
            return
        # Manage the cartesian translation
        (a1, a2) = cartesian_calc(p.x, p.y)
        if self.debug: print("Arm1: {} Arm2: {}".format(a1,a2))
        if self.debug: print("old arm_1_angle: {} arm_2_angle: {}".format(self.arm_1_angle, self.arm_2_angle))
        # Work out which arm 1 angle difference is smaller.
        diff_1 = abs(wrapping_diff(a1, self.arm_1_angle))
        diff_2 = abs(wrapping_diff(a2, self.arm_1_angle))
        if self.debug: print("diff_1: {} diff_2: {}".format(diff_1, diff_2))
        if diff_1 > diff_2:
            # Swap a1 and a2
            a1, a2 = a2, a1
        self.arm_1_angle = a1
        self.arm_2_angle = a2
        if self.debug: print("new arm_1_angle: {} arm_2_angle: {}".format(self.arm_1_angle, self.arm_2_angle))
        self.s1.set_angle(self.arm_1_angle, pwm_motion=self.pwm_move)
        self.s2.set_angle(self.arm_2_angle, pwm_motion=self.pwm_move)

    def tick(self):
        ticks = ticks_us()
        # Shortcut lazy-evaluation
        done1 = self.s1.go(ticks)
        done2 = self.s2.go(ticks)
        done = done1 and done2
        # TODO Not very happy about this. Revisit it.
        if self.gcode and self.gcode[0] == "G28" and done:
            self.s1.homing = False
            self.s2.homing = False
            self.origin.set_zero()
        if done:
            # Was our last movement directly to the end point of the move?
            if self.target != self.origin and self.move_mode == 2:
                # Check distance to final target:
                if self.target.distance_to(self.origin) < PATH_SPLIT_SIZE:
                    # We're near enough to the end of the move. Go straight there.
                    self.start_move_to_point(self.target)
                else:
                    # We need to take another step towards the target.
                    self.intermediate_target = self.origin + self.move_vector
                    self.start_move_to_point(self.intermediate_target)
            self.pattern_step += 1
            if self.pattern_step < len(self.pattern):
                self.set_gcode(self.pattern[self.pattern_step])
            elif self.gcode != None:
                print("Done running pattern")
                self.gcode = None
        return done