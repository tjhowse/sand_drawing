#!/usr/bin/python3
import paho.mqtt.publish as publish
from constants import *
from generator_libs import *

import secrets
if secrets.wifi_ssid == 'my_ssid':
    import secrets_real as secrets

def pub(topic, payload):
    publish.single( topic=topic,
                    payload=payload,
                    retain=True,
                    hostname=secrets.mqtt_host,
                    port=1883,
                    auth={"username":secrets.mqtt_username, "password":secrets.mqtt_password})
generator_string = """
def generator():
    starting_r = 175
    step = 5
    while True:
        for r in range(starting_r, 0, -step):
            for p in circle_points(r, 8):
                yield g(p)
        for r in range(0, starting_r, step):
            for p in circle_points(r, 8):
                yield g(p)
"""

# generator_string = """
# def generator():
#     yield HOME_X
#     yield HOME_Y
#     while True:
#         for p in circle_points(EDGE_R, 8):
#             yield g(p)
#             yield g(vector2())
# """
# generator_string = """
# def generator():
#     yield HOME_X
#     yield HOME_Y
# """
# generator_string = """
# def generator():
#     print("First call")
#     yield "G28 X"
#     print("Second call")
#     yield "G28 Y"
# """
pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)
# print(generator_string)

# exec(generator_string)
# a = generator()
# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))