#!/usr/bin/python3
import paho.mqtt.publish as publish
import matplotlib.pyplot as plt
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

def visualise(generator_string, n):
    exec(generator_string)
    g = locals()['generator']()
    x_dots = []
    y_dots = []
    for x, y in ENCLOSURE_VERTICES:
        x_dots += [x]
        y_dots += [y]
    x_dots += [ENCLOSURE_VERTICES[0][0]]
    y_dots += [ENCLOSURE_VERTICES[0][1]]
    plt.plot(x_dots, y_dots, linewidth=2, color="red")
    x_dots = []
    y_dots = []
    for i in range(n):
        p = next(g, None)
        if p is None:
            break
        if not p.startswith("G1"):
            continue
        p = p.split(' ')
        x_dots += [float(p[1][1:])]
        y_dots += [float(p[2][1:])]
    plt.plot(x_dots, y_dots, linewidth=1)
    plt.title("Pattern visualisation")
    plt.xlabel("X")
    plt.xlim(-200,200)
    plt.ylabel("Y")
    plt.ylim(-200,200)
    plt.axes().set_aspect('equal')
    plt.show()

def publish_octagonal_spiral():
    generator_string = """
def generator():
    yield HOME_X
    yield HOME_Y
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
    pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)

def publish_spirograph():
    generator_string = """
def generator():
    yield HOME_X
    yield HOME_Y
    max_r = 165

    big_r = int((2*max_r)/4)
    big_angle = 0
    big_step = 1

    little_r = int(max_r/2)
    little_angle = 0
    little_step = 20

    little_centre = vector2()
    little_offset = vector2()
    while True:
        big_angle += big_step
        little_centre.x = big_r*math.sin(math.radians(big_angle))
        little_centre.y = big_r*math.cos(math.radians(big_angle))

        little_angle -= little_step
        little_offset.x = little_r*math.sin(math.radians(little_angle))
        little_offset.y = little_r*math.cos(math.radians(little_angle))

        yield g(little_centre + little_offset)
    """
    # visualise(generator_string,1000)
    pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)

def publish_grid():
    generator_string = """
def generator():
    yield HOME_X
    yield HOME_Y
    max_r = 165
    max_r_sq = max_r**2
    p = vector2()
    step_size = 15
    y = 0
    def seq():
        y = 0
        while True:
            p.x = 0
            p.y = y
            yield p
            p.x = math.sqrt(abs(max_r_sq-y**2))
            p.y = y
            yield p
            y += step_size
            if y > max_r: break
            p.x = math.sqrt(abs(max_r_sq-y**2))
            p.y = y
            yield p
            p.x = 0
            p.y = y
            yield p
            y += step_size
            if y > max_r: break
        yield vector2(0,y)
    while True:
        s = seq()
        for p in s:
            yield g(p)
        s = seq()
        for p in s:
            p.x, p.y = -p.x, -p.y
            yield g(p)
            yield g(p)
        s = seq()
        for p in s:
            p.x, p.y = p.y, -p.x
            yield g(p)
            yield g(p)
        s = seq()
        for p in s:
            p.x, p.y = -p.y, p.x
            yield g(p)

    """
    # visualise(generator_string,300)
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)
publish_grid()
# publish_spirograph()
# pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
# pub(secrets.mqtt_root+"/sand_drawing/generator", "")

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
# print(generator_string)

# exec(generator_string)
# a = generator()
# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))