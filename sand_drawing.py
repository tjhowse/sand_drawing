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

MQTT_ENABLED = False
WIFI_CONNECT_WAIT_MAX_S = 10
NEW_PATTERN_CHECK_INTERVAL_MS = 2000

SAND_DRAWING_TOPIC = secrets.mqtt_root+"/sand_drawing"
PATTERN_TOPIC = bytes(SAND_DRAWING_TOPIC+"/pattern", "utf-8")

G_PATTERN = ""

def main():
    global G_PATTERN
    mqtt = None
    s1 = stepper(A1S_PIN, A1D_PIN, A1O_PIN,False, "X")
    s2 = stepper(A2S_PIN, A2D_PIN, A2O_PIN,False, "Y")
    my_cnc = cnc(s1, s2)

    pattern = [ "G28 X",
                "G28 Y",
                "G16 1",
                "G1 X0 Y0",
                "G1 X60 Y300",
                "G1 X120 Y240",
                "G1 X180 Y180",
                "G1 X240 Y120",
                "G1 X300 Y60",
                "G1 X0 Y0",
                "J0 3",
                ]
    # pattern = ["G28 X", "G28 Y", "G1 X-180 Y360"]
    # pattern = [ "G28 X",
    #             "G28 Y",
    #             "G16 1",
    #             "G1 X90 Y0",
    #             "G1 Y180",
    #             "G1 Y270",
    #             "G1 Y360",
    #             "G1 X180 Y90",
    #             "G1 Y180",
    #             "J0 3",
    #             # "G0 Y270",
    #             # "G0 Y360",
    #             # "G0 X270 Y180",
    #             # "G0 Y180",
    #             "G0 Y270",
    #             "G0 Y0",
    #             "G0 Y90",
    #             "G0 Y180",
    #             "G0 Y90",
    #             "G0 Y0",
    #             "G0 Y270",
    #             "G0 Y180",
    #             "J0 3",
    #             ]
    last_pattern_check_ticks_ms = ticks_ms()
    print("about to loop")
    my_cnc.set_pattern(pattern)

    while True:
        mqtt = mqtt_check(mqtt)
        last_pattern_check_ticks_ms = ticks_ms()
        if G_PATTERN != "":
            print(G_PATTERN)
            pattern = G_PATTERN.split(',')
            pattern_step = 0
            G_PATTERN = ""
            my_cnc.set_pattern(pattern)
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
    c.check_msg()
    return c

def mqtt_callback(topic, msg):
    global G_PATTERN
    print("Got callback: {} {}".format(topic, msg))
    if topic == PATTERN_TOPIC:
        print("New pattern!")
        G_PATTERN = str(bytearray(msg), "utf-8")

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

