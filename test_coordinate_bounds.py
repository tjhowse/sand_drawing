#!/usr/bin/python3

from constants import *
from cnc import *
gcode = ""

for vert in ENCLOSURE_VERTICES:
    gcode += "G1 X{} Y{},".format(vert[0], vert[1])

print(gcode)
print(ENCLOSURE_VERTICES)
print(filter_coordinate((100,100), ENCLOSURE_VERTICES))
print(filter_coordinate((150,180), ENCLOSURE_VERTICES))
# print(filter_coordinate((200,-150), ENCLOSURE_VERTICES))
# print(filter_coordinate((-200,-150), ENCLOSURE_VERTICES))
# print(filter_coordinate((-200,150), ENCLOSURE_VERTICES))

# G28 X, G28 Y,G1 X0 Y175,G1 X123 Y123,G1 X175 Y0,G1 X123 Y-123,G1 X0 Y-175,G1 X-123 Y-123,G1 X-175 Y0,G1 X-123 Y123, J0 2