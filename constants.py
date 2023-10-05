import math
MICROCONTROLLER = "board_v1"
PWM_STEPPING = False

class StepperPins:
    step = 0
    dir = 0
    enable = 0
    cfg1 = 0
    cfg2 = 0
    cfg3 = 0
    opto = 0
if MICROCONTROLLER == "d1mini":
    A1S_PIN = 16
    A1D_PIN = 5
    A2S_PIN = 4
    A2D_PIN = 0
    A1O_PIN = 12
    A2O_PIN = 14
elif MICROCONTROLLER == "atom":
    A1S_PIN = 33
    A1D_PIN = 23
    A2S_PIN = 19
    A2D_PIN = 22
    A1O_PIN = 21
    A2O_PIN = 25
elif MICROCONTROLLER == "board_v1":
    A1PINS = StepperPins()
    A1PINS.step = 16
    A1PINS.dir = 4
    A1PINS.enable = 19
    A1PINS.cfg1 = 18
    A1PINS.cfg2 = 5
    A1PINS.cfg3 = 17
    A1PINS.opto = 36

    A2PINS = StepperPins()
    A2PINS.step = 32
    A2PINS.dir = 12
    A2PINS.enable = 27
    A2PINS.cfg1 = 26
    A2PINS.cfg2 = 25
    A2PINS.cfg3 = 33
    A2PINS.opto = 39


STEPS_PER_REV = 200
WILD_MODE = False
if WILD_MODE:
    MICROSTEPPING = 1
    DEFAULT_MOVE_SPEED = 180
else:
    MICROSTEPPING = 32
    DEFAULT_MOVE_SPEED = 30

GEAR_RATIO = 44/20
REAL_STEPS_PER_REV = int(STEPS_PER_REV*MICROSTEPPING*GEAR_RATIO)
REAL_STEPS_PER_DEGREE = REAL_STEPS_PER_REV/360
HALF_REAL_STEPS_PER_REV = REAL_STEPS_PER_REV/2

INDEX_CLOSE_ENOUGH = 3
HOME_SPEED = 180

# You'll have to tweak these to suit the exact placement of your optoswitches.
ARM1_HOME_INDEX = 0
ARM1_HOME_ANGLE = 0
ARM2_HOME_INDEX = REAL_STEPS_PER_REV/2-120
ARM2_HOME_ANGLE = 180

# This may need adjustment for your enclosure. Mine's a regular octagon.
# If your enclosure is circular (how fancy) you can simplify the bounds-checking
# in the cnc class.
ENCLOSURE_VERTEX_COUNT = 8
# This is the distance of the verticies from the centre.
ENCLOSURE_RADIUS = 180
ENCLOSURE_VERTICES = []
for i in range(ENCLOSURE_VERTEX_COUNT):
    angle = math.radians(i*(360/ENCLOSURE_VERTEX_COUNT))
    x = math.trunc(ENCLOSURE_RADIUS*math.sin(angle))
    y = math.trunc(ENCLOSURE_RADIUS*math.cos(angle))
    ENCLOSURE_VERTICES += [(x,y)]

# Movements will be split into smaller stepwise movements of this length at most
# Lower numbers mean straighter movements but more processing time.
PATH_SPLIT_SIZE = 0.5

ARM_1_LENGTH = 100
ARM_2_LENGTH = 100

MOVE_MODE_RAW_SPEED = 0
MOVE_MODE_RAW_ANGLE = 1
MOVE_MODE_CARTESIAN = 2
MOVE_MODE_POLAR = 3

COORD_MODE_ABSOLUTE = 0
COORD_MODE_RELATIVE = 1