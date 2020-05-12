#!/usr/bin/python3

from constants import *
from cnc import *


print(filter_coordinate((200,150), ENCLOSURE_VERTICES))
print(filter_coordinate((200,-150), ENCLOSURE_VERTICES))
print(filter_coordinate((-200,-150), ENCLOSURE_VERTICES))
print(filter_coordinate((-200,150), ENCLOSURE_VERTICES))
