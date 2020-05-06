# pylint: disable=E0401
from math import acos, atan2, sqrt, pi
from constants import *
from utime import ticks_us, ticks_diff

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

ARM_1_LENGTH = 200
ARM_2_LENGTH = 200

def wrapping_diff(x, y):
    diff = x - y
    return (diff + 180) % 360 - 180


class cnc():
    move_mode = 0
    coord_mode = 0
    debug = True
    gcode = None
    cart_x = 0
    cart_y = 0
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
                            self.cart_x = float(coord[1:])
                        elif coord.startswith('Y'):
                            self.cart_y = float(coord[1:])
                        elif coord.startswith('S'):
                            # This is where the speed of the movement is set.
                            pass

            if self.move_mode == 2:
                if (self.cart_x == self.cart_y == 0):
                    # Handle the zero case.
                    self.arm_2_angle = self.arm_1_angle-180
                    self.s1.set_angle(self.arm_1_angle, pwm_motion=pwm_move)
                    self.s2.set_angle(self.arm_2_angle, pwm_motion=pwm_move)
                else:
                    # Manage the cartesian translation
                    (a1, a2) = cartesian_calc(self.cart_x, self.cart_y)
                    if self.debug: print("Arm1: {} Arm2: {}".format(a1,a2))
                    if self.debug: print("old arm_1_angle: {} arm_2_angle: {}".format(self.arm_1_angle, self.arm_2_angle))
                    # Work out which arm 1 angle difference is smaller.
                    diff_1 = wrapping_diff(a1, self.arm_1_angle)
                    diff_2 = wrapping_diff(a2, self.arm_1_angle)
                    if self.debug: print("diff_1: {} diff_2: {}".format(diff_1, diff_2))
                    if abs(diff_1) < abs(diff_2):
                        self.arm_1_angle = a1
                        self.arm_2_angle = a2
                    else:
                        self.arm_1_angle = a2
                        self.arm_2_angle = a1
                    if self.debug: print("new arm_1_angle: {} arm_2_angle: {}".format(self.arm_1_angle, self.arm_2_angle))
                    self.s1.set_angle(self.arm_1_angle, pwm_motion=pwm_move)
                    self.s2.set_angle(self.arm_2_angle, pwm_motion=pwm_move)
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