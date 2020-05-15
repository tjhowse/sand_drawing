# pylint: disable=E0401

from umqtt.simple import MQTTClient
import time
from utime import ticks_us, ticks_ms, sleep_ms, sleep_us, ticks_diff
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
PATTERN_TOPIC = bytes(SAND_DRAWING_TOPIC+"/pattern", "utf-8")
GENERATOR_TOPIC = bytes(SAND_DRAWING_TOPIC+"/generator", "utf-8")

G_PATTERN = ""
G_GENERATOR = ""

def main():
    global G_PATTERN
    global G_GENERATOR
    mqtt = None
    generator = None
    s1 = stepper(A1S_PIN, A1D_PIN, A1O_PIN, False, "X", ARM1_HOME_INDEX, ARM1_HOME_ANGLE)
    s2 = stepper(A2S_PIN, A2D_PIN, A2O_PIN, False, "Y", ARM2_HOME_INDEX, ARM2_HOME_ANGLE)
    my_cnc = cnc(s1, s2)
    pattern = [ "G28 X",
                "G28 Y",
                "G16 2",
                "G1 X1 Y1",
                "G1 X1000 Y1000",
                "J0 3",
                ]
    last_pattern_check_ticks_ms = ticks_ms()
    print("about to loop")
    my_cnc.set_pattern(pattern)

    while True:
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
            generator = G_GENERATOR
            pattern = []
            my_cnc.set_generator(generator)
            G_GENERATOR = ""
        while not my_cnc.tick():
            if ticks_diff(ticks_ms(), last_pattern_check_ticks_ms) > NEW_PATTERN_CHECK_INTERVAL_MS:
                mqtt = mqtt_check(mqtt)
                last_pattern_check_ticks_ms = ticks_ms()

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
        broker.publish(topic, b'{}'.format(message))
        return broker
    except:
        return None

def mqtt_connect():
    print("Attempting connection to MQTT broker")
    c = MQTTClient( secrets.mqtt_clientid,
                    secrets.mqtt_host, 1883,
                    secrets.mqtt_username,
                    secrets.mqtt_password, 0, ssl=False)
    c.set_callback(mqtt_callback)
    c.connect(clean_session=False)
    c.subscribe(PATTERN_TOPIC)
    c.subscribe(GENERATOR_TOPIC)
    c.check_msg()
    return c

def mqtt_callback(topic, msg):
    print("Got callback: {} {}".format(topic, msg))
    if topic == PATTERN_TOPIC:
        print("New pattern!")
        global G_PATTERN
        G_PATTERN = str(bytearray(msg), "utf-8")
    elif topic == GENERATOR_TOPIC:
        print("New generator!")
        global G_GENERATOR
        G_GENERATOR = str(bytearray(msg), "utf-8")

def save_pattern(id, pattern):
    with open("pattern_"+str(id), 'w') as f:
        f.write(pattern)

def load_pattern(id):
    try:
        with open("pattern_"+str(id), 'r') as f:
            return f.read()
    except:
        return ""

def wifi_connect():
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
        raise("Connection failed")

