#!/usr/bin/python3

from constants import *
from cnc import *
print(ENCLOSURE_VERTICES)
print(filter_coordinate((100,100), ENCLOSURE_VERTICES))
print(filter_coordinate((150,180), ENCLOSURE_VERTICES))
# print(filter_coordinate((200,-150), ENCLOSURE_VERTICES))
# print(filter_coordinate((-200,-150), ENCLOSURE_VERTICES))
# print(filter_coordinate((-200,150), ENCLOSURE_VERTICES))
