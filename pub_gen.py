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
    coord_mode = COORD_MODE_ABSOLUTE
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
        if p.startswith("G90"):
            coord_mode = COORD_MODE_ABSOLUTE
        elif p.startswith("G91"):
            coord_mode = COORD_MODE_RELATIVE
        if not p.startswith("G1"):
            continue
        p = p.split(' ')
        x = float(p[1][1:])
        y = float(p[2][1:])
        if coord_mode == COORD_MODE_RELATIVE and len(x_dots) > 0:
            x += x_dots[-1]
            y += y_dots[-1]
        x_dots += [x]
        y_dots += [y]
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
    # yield HOME_X
    # yield HOME_Y
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

def publish_circular_spiral():
    generator_string = """
def generator():
    # yield HOME_X
    # yield HOME_Y
    starting_r = 200
    step = 5
    while True:
        for r in range(starting_r, 0, -step):
            for p in circle_points(r, 128):
                yield g(p)
        for r in range(0, starting_r, step):
            for p in circle_points(r, 128):
                yield g(p)
"""
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)
# publish_circular_spiral()
# exit(0)

def publish_spirograph():
    generator_string = """
def generator():
    # yield HOME_X
    # yield HOME_Y
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
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    # pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)
# publish_spirograph()
# exit(0)

def publish_grid():
    generator_string = """
def generator():
    # yield HOME_X
    # yield HOME_Y
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
        for rotate in [True, False]:
            for i,j,flip in [(1,1,False), (-1,-1,False), (1,-1,True),(-1,1,True)]:
                s = seq()
                for p in s:
                    if flip:
                        if rotate:
                            p.y, p.x = i*p.y, j*p.x
                        else:
                            p.x, p.y = i*p.y, j*p.x
                    else:
                        if rotate:
                            p.y, p.x = i*p.x, j*p.y
                        else:
                            p.x, p.y = i*p.x, j*p.y
                    yield g(p)

    """
    # visualise(generator_string,150)
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)
# publish_grid()
# exit(0)

def publish_wave():
    generator_string = """
def generator():
    max_r = 165
    big_r = int(max_r/2)
    # yield HOME_X
    # yield HOME_Y
    yield g(vector2())

    centre = vector2()
    offset = vector2()
    while True:
        for j in range(0, 360, 10):
            centre.x = big_r*math.sin(math.radians(j))
            centre.y = big_r*math.cos(math.radians(j))
            for i in range(0,180,3):
                offset.x = big_r*math.sin(math.radians(i+j))
                offset.y = big_r*math.cos(math.radians(i+j))
                yield g(centre + offset)
    """
    # visualise(generator_string,10000)
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)

# publish_wave()
# exit(0)

def publish_rotating_poly():
    generator_string = """
def generator():
    max_r = 165
    vertex_count = 3
    # yield HOME_X
    # yield HOME_Y
    yield g(vector2())
    corner = vector2()
    while True:
        for j in range(0, 360, 10):
            for i in range(vertex_count):
                corner.x = max_r*math.sin(math.radians(j+i*(360/vertex_count)))
                corner.y = max_r*math.cos(math.radians(j+i*(360/vertex_count)))
                print(corner)
                yield g(corner)
    """
    # visualise(generator_string,100)
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)

# publish_rotating_poly()
# exit(0)

def publish_contracting_swirls():
    generator_string = """
def generator():
    # yield HOME_X
    # yield HOME_Y
    max_r = 165
    shrink_step = 40
    little_r = shrink_step/2
    big_r = int(max_r - little_r)

    big_circle_angle_step = 5
    little_circle_angle_step = 20

    little_centre = vector2()
    little_offset = vector2()
    while True:
        r = big_r
        j = 0
        while r > 0:
            little_circle_count = (math.pi*r*2)/(little_r)
            big_circle_angle_step = (360/little_circle_count)
            j += big_circle_angle_step
            little_centre.x = r*math.sin(math.radians(j))
            little_centre.y = r*math.cos(math.radians(j))

            for i in range(0, 360, little_circle_angle_step):
                little_offset.x = little_r*math.sin(math.radians(i+j))
                little_offset.y = little_r*math.cos(math.radians(i+j))
                yield g(little_centre + little_offset)

            r -= shrink_step/int(360/big_circle_angle_step)
            # Circumference divided by the radius of the little circle gives
            # the number of circles we want at each layer
        r = little_r
        while r < big_r:
            little_circle_count = (math.pi*r*2)/(little_r)
            big_circle_angle_step = (360/little_circle_count)
            j += big_circle_angle_step
            little_centre.x = r*math.sin(math.radians(j))
            little_centre.y = r*math.cos(math.radians(j))

            for i in range(0, 360, little_circle_angle_step):
                little_offset.x = little_r*math.sin(math.radians(i+j))
                little_offset.y = little_r*math.cos(math.radians(i+j))
                yield g(little_centre + little_offset)

            r += shrink_step/int(360/big_circle_angle_step)
            # Circumference divided by the radius of the little circle gives
            # the number of circles we want at each layer
        r = big_r

    """
    # visualise(generator_string,200000)
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)
# publish_contracting_swirls()
# exit(0)


def publish_relative_motion_test():
    generator_string = """
def generator():
    yield HOME_X
    yield HOME_Y
    yield "G91"
    while True:
        yield g(vector2(0,0))
        yield g(vector2(0,10))
        yield g(vector2(10,0))
        yield g(vector2(10,10))
        yield g(vector2(50,50))
        yield g(vector2(0,-100))
        yield g(vector2(-70,30))
    """
    # visualise(generator_string,200000)
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)

publish_relative_motion_test()