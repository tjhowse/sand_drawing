# pylint: disable=E0401

from umqtt.simple import MQTTClient
import time
import os
import random
from utime import ticks_us, ticks_ms, sleep_ms, sleep_us, ticks_diff, time
import machine
import network
import secrets
if secrets.wifi_ssid == 'my_ssid':
    import secrets_real as secrets

from constants import *

from stepper import stepper
from cnc import cnc

MQTT_ENABLED = True
WIFI_CONNECT_WAIT_MAX_S = 10
NEW_PATTERN_CHECK_INTERVAL_MS = 2000

SAND_DRAWING_TOPIC = secrets.mqtt_root+"/sand_drawing"

# These are volatile variables written to from callbacks.
g_shuffle_generator_interval_s = -1
g_last_generator_shuffle_s = 0
g_stepper_config = ''

def get_generator_file_list():
    return [filename for filename in os.listdir() if filename.endswith(".pat")]

def do_pattern(msg):
    global G_PATTERN
    global g_shuffle_generator_interval_s
    G_PATTERN = str(bytearray(msg), "utf-8")
    g_shuffle_generator_interval_s = -1

def do_generator(msg):
    global G_GENERATOR
    global g_shuffle_generator_interval_s
    G_GENERATOR = str(bytearray(msg), "utf-8")
    g_shuffle_generator_interval_s = -1

def do_save_generator(msg):
    msg = str(bytearray(msg), "utf-8")
    filename, generator = msg.split(' ',1)
    if not filename.endswith(".pat"):
        return
    with open(str(filename), 'wb') as f:
        f.write(generator)

def do_run_generator(msg):
    filename = str(bytearray(msg), "utf-8")
    return do_run_generator_internal(filename)

def do_run_generator_internal(filename):
    global G_GENERATOR
    print("Running generator: "+filename)
    print("Running generator decoded: "+filename)
    if not filename in get_generator_file_list():
        print("Generator not found")
        return
    print("Running generator from flash {}".format(filename))
    with open(str(filename), 'r') as f:
        G_GENERATOR = f.read()


def do_list_generators(filename):
    global G_PUBLISH
    gen_list = str(get_generator_file_list())
    G_PUBLISH = (bytes(SAND_DRAWING_TOPIC+"/generator_list", "utf-8"), bytes(gen_list, "utf-8"))

def do_delete_generator(filename):
    if not filename.endswith(".pat"):
        return
    os.remove(filename)

def do_shuffle_generators(msg=''):
    print("Shuffling generators")
    global g_shuffle_generator_interval_s
    global g_last_generator_shuffle_s
    g_last_generator_shuffle_s = time()
    generators = get_generator_file_list()
    print("Got list")
    if not generators:
        print("No generators found")
        return
    print("picking random generator")
    random_generator = random.choice(generators)
    print("Random generator: "+random_generator)
    do_run_generator_internal(random_generator)
    print("Ran generator")
    if len(msg) > 0:
        print("Set shuffle interval: "+str(msg))
        g_shuffle_generator_interval_s = int(msg)
    print("Shuffle interval: {}".format(g_shuffle_generator_interval_s))

def do_stepper_config(msg=''):
    if not MICROCONTROLLER.startswith("board_v1_2"):
        return
    global g_stepper_config
    new_config = str(bytearray(msg), "utf-8").split(',')
    if len(new_config) != 4:
        g_stepper_config = ''
    else:
        g_stepper_config = new_config


def save_pattern(id, pattern):
    with open("pattern_"+str(id), 'w') as f:
        f.write(pattern)

def load_pattern(id):
    try:
        with open("pattern_"+str(id), 'r') as f:
            return f.read()
    except:
        return ""

# A list of tuples of (<topic>, <callback function>)
SUBSCRIPTIONS = []
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/pattern", "utf-8"), do_pattern)]
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/generator", "utf-8"), do_generator)]
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/save_generator", "utf-8"), do_save_generator)]
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/list_generators", "utf-8"), do_list_generators)]
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/delete_generator", "utf-8"), do_delete_generator)]
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/run_generator", "utf-8"), do_run_generator)]
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/shuffle_generators", "utf-8"), do_shuffle_generators)]
SUBSCRIPTIONS += [(bytes(SAND_DRAWING_TOPIC+"/stepper_config", "utf-8"), do_stepper_config)]

G_PATTERN = ""
G_GENERATOR = ""
G_PUBLISH = ('','')

def main():
    global G_PATTERN
    global G_GENERATOR
    global G_PUBLISH
    global g_shuffle_generator_interval_s
    global g_last_generator_shuffle_s
    global g_stepper_config
    mqtt = None
    generator = None
    s1 = stepper(A1PINS, False, "X", ARM1_HOME_INDEX, ARM1_HOME_ANGLE)
    s2 = stepper(A2PINS, False, "Y", ARM2_HOME_INDEX, ARM2_HOME_ANGLE)
    my_cnc = cnc(s1, s2)
    pattern = [ "G1 X1 Y1",
                "G1 X1000 Y1000",
                "J0 0",
                ]
    last_pattern_check_ticks_ms = 0
    print("about to loop")
    # Force a home on startup
    my_cnc.set_gcode("G28 X")
    my_cnc.block_until_done()
    my_cnc.set_gcode("G28 Y")
    my_cnc.block_until_done()
    # Set cartesian mode
    my_cnc.set_gcode("G16 2")

    my_cnc.set_pattern(pattern)

    while True:
        if g_shuffle_generator_interval_s > 0:
            if (time() - g_last_generator_shuffle_s) > g_shuffle_generator_interval_s:
                do_shuffle_generators()
        if ticks_diff(ticks_ms(), last_pattern_check_ticks_ms) > NEW_PATTERN_CHECK_INTERVAL_MS:
            mqtt = mqtt_check(mqtt)
            last_pattern_check_ticks_ms = ticks_ms()
            if G_PATTERN != "":
                generator = ""
                print(G_PATTERN)
                pattern = G_PATTERN.split(',')
                pattern = [a.strip() for a in pattern]
                G_PATTERN = ""
                my_cnc.set_pattern(pattern)
            if G_GENERATOR != "":
                if generator != G_GENERATOR:
                    generator = G_GENERATOR
                    pattern = []
                    my_cnc.set_generator(generator)
                G_GENERATOR = ""
            if G_PUBLISH != ('',''):
                try:
                    mqtt.publish(G_PUBLISH[0], G_PUBLISH[1])
                finally:
                    G_PUBLISH = ('','')
            if g_stepper_config != '':
                try:
                    if g_stepper_config[0] == '1':
                        s1.config(g_stepper_config[1:])
                    elif g_stepper_config[0] == '2':
                        s2.config(g_stepper_config[1:])
                finally:
                    g_stepper_config = ''
        my_cnc.tick()

def mqtt_check(mqtt):
    if not MQTT_ENABLED:
        return None
    wifi_connect()
    if mqtt == None:
        try:
            mqtt = mqtt_connect()
            mqtt.check_msg()
            print("Successfully connected to broker")
        except Exception as e :
            print("Couldn't connect to broker. Try again later: {}".format(e))
            mqtt = None
    else:
        try:
            mqtt.check_msg()
        except:
            mqtt = None
    return mqtt

def robust_publish(broker, topic, message):
    if broker == None:
        return None
    try:
        # Skip pylint error because we're running micropython
        # pylint: disable=E1101
        broker.publish(topic, b'{}'.format(message))
        return broker
    except Exception as e:
        print("Couldn't publish to broker: {}".format(e))
        return None

def mqtt_connect():
    print("Attempting connection to MQTT broker")
    c = MQTTClient( secrets.mqtt_clientid,
                    secrets.mqtt_host, 1883,
                    secrets.mqtt_username,
                    secrets.mqtt_password, 0, ssl=False)
    c.set_callback(mqtt_callback)
    c.connect(clean_session=False)
    for topic, callback in SUBSCRIPTIONS:
        c.subscribe(topic)
    c.check_msg()
    return c

def mqtt_callback(topic, msg):
    print("Got callback: {} {}".format(topic, msg))
    for cb_topic, callback in SUBSCRIPTIONS:
        if cb_topic == topic:
            callback(msg)
            return

def wifi_connect():
    # Lots of potential for improvement here. We should cache the wifi object, for starters.
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        return
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if.active(True)
    sta_if.connect(secrets.wifi_ssid, secrets.wifi_password)
    start_time = ticks_ms()
    while ticks_diff(ticks_ms(), start_time) < WIFI_CONNECT_WAIT_MAX_S*1000:
        if sta_if.isconnected():
            break
        sleep_ms(100)
    else:
        # We failed to connect.
        # Skip pylint error because we're running micropython
        # pylint: disable=E702
        raise(Exception("Connection failed"))
    print("Connected to wifi")
