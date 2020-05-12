#!/usr/bin/python3

from constants import *
from cnc import *

point = (200,-150)

a = filter_coordinate(point, ENCLOSURE_VERTICES)
print(a)
