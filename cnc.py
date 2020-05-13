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
    def vectorTo(self, p):
        return vector2(p.x-self.x, p.y-self.y)
    def magnitude(self):
        return sqrt(self.x*self.x+self.y*self.y)
    def set_magnitude(self, m):
        scale = m/self.magnitude()
        self.x *= scale
        self.y *= scale
    def cap_magnitude(self, m):
        if self.magnitude() > m:
            self.set_magnitude(m)


class cnc():
    move_mode = 0
    coord_mode = 0
    debug = True
    gcode = None
    origin = vector2()
    vector = vector2()
    target = vector2()
    arm_1_angle = 0
    arm_2_angle = 0

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
            pwm_move = self.gcode[0] == "G0"
            if len(self.gcode) == 1:
                return
            for coord in self.gcode[1:]:
                if self.coord_mode == 0:
                    if self.move_mode == 0:
                        # Continuous raw movement
                        if coord.startswith('X'):
                            self.s1.set_speed(float(coord[1:]), pwm_motion=pwm_move)
                        elif coord.startswith('Y'):
                            self.s2.set_speed(float(coord[1:]), pwm_motion=pwm_move)
                    elif self.move_mode == 1:
                        # Discrete raw movement
                        if coord.startswith('X'):
                            self.arm_1_angle = float(coord[1:])
                            self.s1.set_angle(self.arm_1_angle, pwm_motion=pwm_move)
                        elif coord.startswith('Y'):
                            self.arm_2_angle = float(coord[1:])
                            self.s2.set_angle(self.arm_2_angle, pwm_motion=pwm_move)
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
                self.move_vector = self.origin.vectorTo(self.target)
                self.move_vector.cap_magnitude(PATH_SPLIT_SIZE)

                if (self.target.x == self.target.y == 0):
                    # Handle the zero case.
                    self.arm_2_angle = self.arm_1_angle-180
                    self.s1.set_angle(self.arm_1_angle, pwm_motion=pwm_move)
                    self.s2.set_angle(self.arm_2_angle, pwm_motion=pwm_move)
                else:
                    # Manage the cartesian translation
                    (a1, a2) = cartesian_calc(self.target.x, self.target.y)
                    if self.debug: print("Arm1: {} Arm2: {}".format(a1,a2))
                    if self.debug: print("old arm_1_angle: {} arm_2_angle: {}".format(self.arm_1_angle, self.arm_2_angle))
                    # Work out which arm 1 angle difference is smaller.
                    diff_1 = abs(wrapping_diff(a1, self.arm_1_angle))
                    diff_2 = abs(wrapping_diff(a2, self.arm_1_angle))
                    if self.debug: print("diff_1: {} diff_2: {}".format(diff_1, diff_2))
                    if diff_1 > diff_2:
                        # Swap a1 and a2
                        a1, a2 = a2, a1
                    arm_1_travel = abs(wrapping_diff(a1, self.arm_1_angle))
                    arm_2_travel = abs(wrapping_diff(a2, self.arm_2_angle))
                    # This is the total travel distance for both steppers
                    total_angle_travel = arm_1_travel+arm_2_travel
                    # TODO This calculation isn't working well enough
                    # We need to move directly between points, this half-measure is insufficient.
                    # Put this into your brain: http://www.machinebuilding.net/ta/t0323.htm
                    # Or maybe this suspiciously similar one: https://www.pmdcorp.com/resources/type/articles/resources/get/motion-kinematics-article
                    if total_angle_travel != 0:
                        arm_1_speed = DEFAULT_MOVE_SPEED*(arm_1_travel/total_angle_travel)
                        arm_2_speed = DEFAULT_MOVE_SPEED*(arm_2_travel/total_angle_travel)
                    else:
                        arm_1_speed = 0
                        arm_2_speed = 0
                    self.arm_1_angle = a1
                    self.arm_2_angle = a2
                    if self.debug: print("diff_1: {} diff_2: {} total: {}".format(diff_1, diff_2, total_angle_travel))
                    if self.debug: print("new arm_1_angle: {} arm_2_angle: {}".format(self.arm_1_angle, self.arm_2_angle))
                    self.s1.set_angle(self.arm_1_angle, speed=arm_1_speed, pwm_motion=pwm_move)
                    self.s2.set_angle(self.arm_2_angle, speed=arm_2_speed, pwm_motion=pwm_move)
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

    def tick(self):
        ticks = ticks_us()
        # Shortcut lazy-evaluation
        done1 = self.s1.go(ticks)
        done2 = self.s2.go(ticks)
        done = done1 and done2
        # Not very happy about this. Revisit it.
        if self.gcode and self.gcode[0] == "G28" and done:
            self.s1.homing = False
            self.s2.homing = False
        if done:
            self.pattern_step += 1
            if self.pattern_step < len(self.pattern):
                self.set_gcode(self.pattern[self.pattern_step])
            elif self.gcode != None:
                print("Done running pattern")
                self.gcode = None


        return done