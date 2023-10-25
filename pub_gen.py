#!/usr/bin/python3
import paho.mqtt.publish as publish
import matplotlib.pyplot as plt
from constants import *
from generator_libs import *

import secrets_example as secrets
if secrets.wifi_ssid == 'my_ssid':
    import secrets_real as secrets

def pub(topic, payload, retain=True):
    publish.single( topic=topic,
                    payload=payload,
                    retain=retain,
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
    # plt.axes().set_aspect('equal')
    plt.gca().set_aspect("equal")
    plt.show()
# dict[str, str]
generators = {}
generators["octaspiral"] = """
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
generators["circular_spiral"] = """
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
generators["spirograph"] = """
def generator():
    # yield HOME_X
    # yield HOME_Y
    max_r = ENCLOSURE_RADIUS

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
generators["grid"] = """
def generator():
    # yield HOME_X
    # yield HOME_Y
    max_r = ENCLOSURE_RADIUS
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
generators["wave"] = """
def generator():
    max_r = ENCLOSURE_RADIUS
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
generators["rotpoly"] = """
def generator():
    max_r = ENCLOSURE_RADIUS
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

generators["contraswirls"] = """
def generator():
    # yield HOME_X
    # yield HOME_Y
    max_r = ENCLOSURE_RADIUS
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

# def publish_relative_motion_test():
#     generator_string = """
# def generator():
#     yield HOME_X
#     yield HOME_Y
#     yield "G91"
#     while True:
#         yield g(vector2(0,0))
#         yield g(vector2(0,10))
#         yield g(vector2(10,0))
#         yield g(vector2(10,10))
#         yield g(vector2(50,50))
#         yield g(vector2(0,-100))
#         yield g(vector2(-70,30))
#     """
#     # visualise(generator_string,200000)
#     # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
#     pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)

# # publish_relative_motion_test()
generators["contrawaves"] = """
def generator():
    # yield HOME_X
    # yield HOME_Y
    min_r = 10
    r_rate = 0.03
    a = 0
    a_rate = 1
    point = vector2()
    wave_size = 5
    wave_rate = 30 # Waves per revolution
    max_r = ENCLOSURE_RADIUS-wave_size
    r = max_r

    while True:
        while r > min_r:
            r -= r_rate
            a = (a+a_rate)%360
            r_mod = wave_size*math.cos(math.radians(a*wave_rate))

            point.x = (r+r_mod)*math.cos(math.radians(a))
            point.y = (r+r_mod)*math.sin(math.radians(a))

            yield g(point)
        while r < max_r:
            r += r_rate
            a = (a+a_rate)%360
            r_mod = wave_size*math.cos(math.radians(a*wave_rate))

            point.x = (r+r_mod)*math.cos(math.radians(a))
            point.y = (r+r_mod)*math.sin(math.radians(a))

            yield g(point)

"""

generators["rotshinkpoly"] = """
def generator():
    max_r = ENCLOSURE_RADIUS
    vertex_count = 4
    # yield HOME_X
    # yield HOME_Y
    corner = vector2()
    r = max_r
    r_step = 5
    min_r = 10

    while True:
        while r > min_r:
            for j in range(0, 360, 10):
                r -= r_step
                for i in range(vertex_count):
                    corner.x = r*math.sin(math.radians(j+i*(360/vertex_count)))
                    corner.y = r*math.cos(math.radians(j+i*(360/vertex_count)))
                    yield g(corner)
        while r < max_r:
            for j in range(0, 360, 10):
                r += r_step
                for i in range(vertex_count):
                    corner.x = r*math.sin(math.radians(j+i*(360/vertex_count)))
                    corner.y = r*math.cos(math.radians(j+i*(360/vertex_count)))
                    yield g(corner)

"""

def publish_circle_grid():
    generator_string = """
def generator():
    max_r = ENCLOSURE_RADIUS
    vertex_count = 4
    # yield HOME_X
    # yield HOME_Y
    centre = vector2()
    offset = vector2()
    circles_n = 4
    small_r = max_r/(circles_n*2-1)
    # big_r
    a = 0
    big_a = 0
    big_a_step = 45

    while True:
        for i in range(circles_n):
            for a in range(180):
                offset.x = small_r*math.sin(math.radians(a))
                offset.y = small_r*math.cos(math.radians(a))
                yield g((centre+offset).rotate(big_a))
            centre.y -= small_r*2
        centre.y += small_r*2
        for i in range(circles_n):
            for a in range(180,360,1):
                offset.x = small_r*math.sin(math.radians(a))
                offset.y = small_r*math.cos(math.radians(a))
                yield g((centre+offset).rotate(big_a))
            centre.y += small_r*2
        centre.y -= small_r*2
        big_a = (big_a+big_a_step)%360
    """
    # visualise(generator_string,20000)
    # pub(secrets.mqtt_root+"/sand_drawing/pattern", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string)
    # pub(secrets.mqtt_root+"/sand_drawing/save_generator", "rotshinkpoly.pat {}".format(generator_string), False)

# This needs more work. Rotation is not the way.
#publish_circle_grid()

def publish_random_spiral_start():
    generator_string = """
def generator():
    import random
    min_r = 5
    max_r = ENCLOSURE_RADIUS
    r_rate = 0.01
    # Don't start a spiral this close to the centre
    keepout_r = 30

    centre = vector2()
    offset = vector2()
    while True:
        r = random.randint(keepout_r, max_r)
        a = random.uniform(0,360)
        centre.x = r*math.sin(a)
        centre.y = r*math.cos(a)
        r = min_r
        offset = vector2(min_r,0)
        mag = min_r
        while inside_convex_polygon(centre+offset, ENCLOSURE_VERTICES):
            yield g(centre+offset)
            offset.rotate(1)
            mag += r_rate
            offset.set_magnitude(mag)
    """
    # visualise(generator_string,10000)
    # pub(secrets.mqtt_root+"/sand_drawing/generator", "")
    pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string, False)

# publish_random_spiral_start()


# http://www.personal.psu.edu/dpl14/java/parametricequations/spirograph/index.html
# Oooh: http://www.davekoelle.com/spiral.html
# Params is a list of 2-tuples containing the radius of the arm and the speed at which
# it rotates relative to the other arms.
generators["spirograph_2"] = """
def generator():
    max_r = ENCLOSURE_RADIUS
    point = vector2()
    step = 0
    # Saved as spirograph_2
    params = [(80,0.025), (20,-0.15), (50,0.23)]
    # params = [(40,0.05), (50,-0.25), (30,0.12), (80,-0.1)]
    # params = [(90,0.05), (40,-0.07), (50,-0.12), (30,-0.2)]

    # Get the sum of all the radii
    total_rad = 0
    for rad, speed in params:
        total_rad += rad
    # Use this to scale each radius so we don't draw outside the bed even when
    # all the radii line up straight.
    scale = max_r/total_rad

    while True:
        point.x = 0
        point.y = 0
        for rad, speed in params:
            point.x += (rad*scale)*math.sin(speed*step)
            point.y += (rad*scale)*math.cos(speed*step)
        yield g(point)
        step += 1
"""

generators["chatgpt1"] = """
def generator():
    # Lissajous curve parameters
    a = 3  # Ratio of frequencies for the X-axis
    b = 2  # Ratio of frequencies for the Y-axis
    max_t = 2 * math.pi  # Maximum parameter value (controls the number of loops)

    rotation_speed = 0.02  # Adjust to control the rotation speed

    t = 0
    while True:
        # Scale the Lissajous curve to fit within ENCLOSURE_RADIUS
        radius = (ENCLOSURE_RADIUS - 10) / 2  # Subtracting 10 for padding
        x = radius * math.sin(a * t)
        y = radius * math.cos(b * t)

        # Rotate the Lissajous curve
        rotation_matrix = [[math.cos(rotation_speed), -math.sin(rotation_speed)],
                            [math.sin(rotation_speed), math.cos(rotation_speed)]]
        rotated_x, rotated_y = x * rotation_matrix[0][0] + y * rotation_matrix[0][1], x * rotation_matrix[1][0] + y * rotation_matrix[1][1]

        yield g(vector2(rotated_x, rotated_y))  # Yield the rotated point in G-code format

        t += 0.01
        if t >= max_t:
            t = 0  # Reset the parameter to restart the pattern


"""

# for name, generator_string in generators.items():
#     pub(secrets.mqtt_root+"/sand_drawing/save_generator", "{}.pat {}".format(name, generator_string), False)

visualise(generators['chatgpt1'], 10000)
    # visualise(generator_string,100000)
    # pub(secrets.mqtt_root+"/sand_drawing/generator", "")
    # pub(secrets.mqtt_root+"/sand_drawing/generator", generator_string, False)
    # pub(secrets.mqtt_root+"/sand_drawing/save_generator", "spirograph_2.pat {}".format(generator_string), False)

# publish_publish_spirograph2()
# print(b-a)
# print(a-b)