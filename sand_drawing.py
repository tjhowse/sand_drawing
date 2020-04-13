#!/usr/bin/python3

class pattern:
    # Patterns contain a list of coordinates and a delay
    # x, y, sleep

    # Patterns can also include mode flags:
    # AbsCart, RelCart, AbsPolar, RelPolar, AbsRaw, RelRaw, etc.
    # Cartesian - X and Y in mm. The centre is 0,0.
    # Polar - Angle and Radius.
    # Raw - The angles of each arm.
    # Absolute - An absolute angle or dimension
    # Relative - A change relative to the last dimension
    # Continuous - Relative continuous motion
    # For now I'm only implementing RelRaw, since I have no way to
    # zero the axes.

    # Patterns have an ID to allow them to be set/cleared.
    id = 0
    steps = []
    def __init__(self):
        pass


def setup():
    pass
    # set up MQTT connection

def loop():
    # Look up the
    for step in current_pattern:
        do_step(step)

def do_step(step):

    usleep(step[2])