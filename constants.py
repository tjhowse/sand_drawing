import math
MICROCONTROLLER = "atom"
PWM_STEPPING = False
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

# You'll have to tweak these to suite the exact placement of your optoswitches.
ARM1_HOME_INDEX = REAL_STEPS_PER_REV-40
ARM2_HOME_INDEX = REAL_STEPS_PER_REV/2-150

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
PATH_SPLIT_SIZE = 1