import math
MICROCONTROLLER = "board_v1_2"
PWM_STEPPING = False

class StepperPins:
    step = 0
    dir = 0
    enable = 0
    cfg1 = 0
    cfg2 = 0
    cfg3 = 0
    opto = 0
    rst = 0 # Reset
    slp = 0 # Sleep
    hall_effect = False


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
    A1PINS.hall_effect = True

    A2PINS = StepperPins()
    A2PINS.step = 32
    A2PINS.dir = 12
    A2PINS.enable = 27
    A2PINS.cfg1 = 26
    A2PINS.cfg2 = 25
    A2PINS.cfg3 = 33
    A2PINS.opto = 39
    A2PINS.hall_effect = True

elif MICROCONTROLLER == "board_v1_2":
    # Note these pin numbers are the "IOXX" numbers, not the pin numbers
    # on the package.
    A1PINS = StepperPins()
    A1PINS.step = 2
    A1PINS.dir = 15
    A1PINS.enable = 19
    A1PINS.cfg1 = 18
    A1PINS.cfg2 = 5
    A1PINS.cfg3 = 17
    A1PINS.rst = 16
    A1PINS.slp = 4

    A1PINS.opto = 36
    A1PINS.hall_effect = True

    A2PINS = StepperPins()
    A2PINS.step = 25
    A2PINS.dir = 33
    # Pins SCK/CLK, SDO/SD0, SDI/SD1, SHD/SD2, SWP/SD3 and SCS/CMD, namely, GPIO6 to GPIO11 are connected
    # to the integrated SPI flash integrated on the module and are not recommended for other uses
    A2PINS.enable = 9 # SD2, not recommended for use. Might be a mistake.
    A2PINS.cfg1 = 13
    A2PINS.cfg2 = 12
    A2PINS.cfg3 = 14
    A2PINS.rst = 27
    A2PINS.slp = 26

    A2PINS.opto = 39
    A2PINS.hall_effect = True


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
# ARM2_HOME_INDEX = REAL_STEPS_PER_REV/2+500 # Too far clockwise
ARM2_HOME_INDEX = REAL_STEPS_PER_REV/2 # this one might be good?
# ARM2_HOME_INDEX = REAL_STEPS_PER_REV/2+500 # Too far counter-clockwise
# ARM2_HOME_INDEX = REAL_STEPS_PER_REV/2-250
ARM2_HOME_ANGLE = 180

# This may need adjustment for your enclosure. Mine's a regular octagon.
# If your enclosure is circular (how fancy) you can simplify the bounds-checking
# in the cnc class.
# ENCLOSURE_VERTEX_COUNT = 8 # Octagon
ENCLOSURE_VERTEX_COUNT = 64 # Circle (ish)
# This is the distance of the verticies from the centre.
ENCLOSURE_RADIUS = 188
ENCLOSURE_VERTICES = []
for i in range(ENCLOSURE_VERTEX_COUNT):
    angle = math.radians(i*(360/ENCLOSURE_VERTEX_COUNT))
    x = math.trunc(ENCLOSURE_RADIUS*math.sin(angle))
    y = math.trunc(ENCLOSURE_RADIUS*math.cos(angle))
    ENCLOSURE_VERTICES += [(x,y)]

# Movements will be split into smaller stepwise movements of this length at most
# Lower numbers mean straighter movements but more processing time.
PATH_SPLIT_SIZE = 0.5

ARM_1_LENGTH = 94
ARM_2_LENGTH = 94

MOVE_MODE_RAW_SPEED = 0
MOVE_MODE_RAW_ANGLE = 1
MOVE_MODE_CARTESIAN = 2
MOVE_MODE_POLAR = 3

COORD_MODE_ABSOLUTE = 0
COORD_MODE_RELATIVE = 1