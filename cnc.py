# pylint: disable=E0401
from constants import *
from generator_libs import *

try:
    from utime import ticks_us, ticks_diff
except ImportError:
    # This isn't running on-target. We don't need these.
    pass

class cnc():
    move_mode = MOVE_MODE_CARTESIAN
    coord_mode = COORD_MODE_ABSOLUTE
    debug = False
    gcode = None
    origin = vector2()
    move_vector = vector2()
    intermediate_target = vector2()
    target = vector2()
    arm_1_angle = 0
    arm_2_angle = 0
    pwm_move = False # Movement modes using PWM to drive steppers. Faster, less precise.
    generator = None

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def set_pattern(self, new_pattern):
        print(new_pattern)
        self.pattern = new_pattern
        self.pattern_step = 0
        self.set_gcode(self.pattern[self.pattern_step])

    def set_generator(self, new_generator):
        print("Received new generator.")
        self.generator = None
        self.pattern = []
        self.pattern_step = 0
        try:
            # This should set "generator" to a... generator
            exec(new_generator)
            # Don't ask me why this is neccessary. The generator in the string
            # wasn't showing up in scope properly? Iunno.
            self.generator = locals()['generator']()
            self.set_gcode(next(self.generator))
            print("Successfully loaded new generator.")
        except Exception as e:
            print("Failed to exec the generator: {}".format(e))
            self.generator = None

    def set_gcode(self, gcode):
        self.gcode = gcode.split(' ')
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
                if self.move_mode == MOVE_MODE_RAW_SPEED:
                    # Continuous raw movement
                    if coord.startswith('X'):
                        self.s1.set_speed(float(coord[1:]), pwm_motion=self.pwm_move)
                    elif coord.startswith('Y'):
                        self.s2.set_speed(float(coord[1:]), pwm_motion=self.pwm_move)
                elif self.move_mode == MOVE_MODE_RAW_ANGLE:
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
                elif self.move_mode == MOVE_MODE_CARTESIAN:
                    # Absolute cartesian positioning
                    if coord.startswith('X'):
                        self.target.x = float(coord[1:])
                    elif coord.startswith('Y'):
                        self.target.y = float(coord[1:])
                    elif coord.startswith('S'):
                        # This is where the speed of the movement is set.
                        pass

            if self.move_mode == MOVE_MODE_CARTESIAN:
                # TODO translate other movement modes into cartesian points so they can be filtered too.
                if self.debug: print("Unfiltered coordinates: {}".format(self.target))
                if self.coord_mode == COORD_MODE_RELATIVE:
                    self.target += self.origin
                (self.target.x, self.target.y) = filter_coordinate((self.target.x, self.target.y), ENCLOSURE_VERTICES)
                if self.debug: print("Filtered coordinates: {}".format(self.target))
                if self.debug: print("self.origin: {}".format(self.origin))
                self.move_vector = self.origin.vector_to(self.target)
                move_mag = self.move_vector.magnitude()
                if self.debug: print("move_vector: {} move_mag: {}".format(self.move_vector, move_mag))
                if move_mag > PATH_SPLIT_SIZE:
                    # This move needs to be split up. Create a vector for calculating stepwise
                    # movements along this path
                    points = math.ceil(move_mag/PATH_SPLIT_SIZE)
                    if self.debug: print("Path length {} > {}, split into {} chunks".format(move_mag, PATH_SPLIT_SIZE, points))
                    self.move_vector.cap_magnitude(move_mag/points)
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
        elif self.gcode[0] == "G90":
            # Absolute movement mode (default)
            self.coord_mode = COORD_MODE_ABSOLUTE
        elif self.gcode[0] == "G91":
            self.coord_mode = COORD_MODE_RELATIVE

    def start_move_to_point(self, p):
        if self.debug: print("Setting origin to {}".format(p))
        self.origin.copy(p)
        if (p.x == p.y == 0):
            # Handle the zero case.
            self.arm_2_angle = self.arm_1_angle-180
            self.s1.set_angle(self.arm_1_angle, pwm_motion=self.pwm_move)
            self.s2.set_angle(self.arm_2_angle, pwm_motion=self.pwm_move)
            return
        # Manage the cartesian translation
        (a1, a2) = cartesian_calc(p.x, p.y)
        # Work out which arm 1 angle difference is smaller.
        diff_1 = abs(wrapping_diff(a1, self.arm_1_angle))
        diff_2 = abs(wrapping_diff(a2, self.arm_1_angle))
        if diff_1 > diff_2:
            # Swap a1 and a2
            a1, a2 = a2, a1
        self.arm_1_angle = a1
        self.arm_2_angle = a2
        self.s1.set_angle(self.arm_1_angle, pwm_motion=self.pwm_move)
        self.s2.set_angle(self.arm_2_angle, pwm_motion=self.pwm_move)

    def get_next_gcode(self):
        if self.generator != None:
            gcode = next(self.generator)
            if gcode != "END":
                self.set_gcode(gcode)
            else:
                print("Done running generator")
                self.gcode = None
        else:
            self.pattern_step += 1
            if self.pattern_step < len(self.pattern):
                self.set_gcode(self.pattern[self.pattern_step])
            elif self.gcode != None:
                print("Done running pattern")
                self.gcode = None

    def tick(self):
        ticks = ticks_us()
        # Shortcut lazy-evaluation
        done1 = self.s1.go(ticks)
        done2 = self.s2.go(ticks)
        done = done1 and done2
        if done:
            # Did we just finish a G0 or G1 instruction? If so, can we calculate the next step
            # or do we need to get a new gcode?
            if self.gcode and self.gcode[0] in ["G0", "G1"]:
                # Was our last movement directly to the end point of the move?
                if self.target != self.origin and self.move_mode == MOVE_MODE_CARTESIAN:
                    # Check distance to final target:
                    if self.target.distance_to(self.origin) < PATH_SPLIT_SIZE:
                        # We're near enough to the end of the move. Go straight there.
                        self.start_move_to_point(self.target)
                    else:
                        # We need to take another step towards the target.
                        self.intermediate_target = self.origin + self.move_vector
                        self.start_move_to_point(self.intermediate_target)
                    return False
            elif self.gcode and self.gcode[0] == "G28":
                if self.s1.indexed and self.s2.indexed:
                    self.start_move_to_point(vector2())
            self.get_next_gcode()
        return done