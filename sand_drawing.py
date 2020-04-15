from umqtt.simple import MQTTClient
import time
from utime import ticks_us, ticks_ms, sleep_ms, sleep_us, ticks_diff
import machine
import network
import secrets
if secrets.wifi_ssid == 'my_ssid':
    import secrets_real as secrets

class pattern:
    # Patterns contain a list of coordinates and a delay
    # x, y, sleep

    # Patterns can also include mode flags:
    # AbsCart, RelCart, AbsPolar, RelPolar, AbsRaw, RelRaw, etc.
    # Cartesian - X and Y in mm. The centre is 0,0.
    # Polar - Angle and Radius.
    # Raw - The angles of each arm.
    # Absolute - An absolute angle or dimension
    # Relative - A change relative to the last dimension
    # Continuous - Relative continuous motion
    # For now I'm only implementing RelRaw, since I have no way to
    # zero the axes.

    # Patterns have an ID to allow them to be set/cleared.
    id = 0
    pattern = ""
    def __init__(self, id, pattern):
        self.id = id
        self.pattern = pattern

A1S_PIN = 16
A1D_PIN = 5
A2S_PIN = 4
A2D_PIN = 0

WIFI_CONNECT_WAIT_MAX_S = 10

SAND_DRAWING_TOPIC = secrets.mqtt_root+"/sand_drawing"
SPEED_TOPIC = SAND_DRAWING_TOPIC+"/speed"
A1DIR_TOPIC = SAND_DRAWING_TOPIC+"/1dir"
A2DIR_TOPIC = SAND_DRAWING_TOPIC+"/2dir"

G_SPEED = 1
G_1DIR = 1
G_2DIR = 1

def main():
    print("Starting up.")
    global G_SPEED, G_1DIR, G_2DIR
    a1s = machine.Pin(A1S_PIN, machine.Pin.OUT)
    a1d = machine.Pin(A1D_PIN, machine.Pin.OUT)
    a2s = machine.Pin(A2S_PIN, machine.Pin.OUT)
    a2d = machine.Pin(A2D_PIN, machine.Pin.OUT)
    # while True:
    #     print('Hi!')
    #     sleep_ms(1000)
    a1d.value(G_1DIR)
    a2d.value(G_2DIR)
    i = 0
    on_1 = True
    dir_1 = 1
    on_2 = True
    dir_2 = 1
    step = 0
    ticks_step = ticks_ms()
    ticks_step_interval = 2000
    while True:
        if ticks_diff(ticks_ms(), ticks_step) > ticks_step_interval:
            ticks_step = ticks_ms()
            step += 1
            print("Step {}".format(step))
            if step == 1:
                on_1 = False
            elif step == 2:
                dir_2 = 0
            elif step == 3:
                on_1 = True
                dir_1 = 0
            elif step == 4:
                on_2 = False
            elif step == 5:
                on_2 = True
                dir_2 = 1
            elif step == 6:
                dir_1 = 1
            elif step == 7:
                on_1 = False
                on_2 = False
            elif step >= 8:
                on_1 = True
                on_2 = True
                step = 0
        a1s.value(0)
        a2s.value(0)
        sleep_ms(G_SPEED)
        if on_1:
            a1s.value(1)
        if on_2:
            a2s.value(1)
        if a1d.value() != dir_1:
            a1d.value(dir_1)
        if a2d.value() != dir_2:
            a2d.value(dir_2)
        sleep_ms(G_SPEED)

    c = None
    while True:
        wifi_connect()
        if c == None:
            try:
                c = mqtt_connect()
                print("Successfully connected to broker")
            except Exception as e :
                print("Couldn't connect to broker. Try again later: {}".format(e))
                c = None
        else:
            try:
                c.check_msg()
            except:
                c = None

        a1d.value(G_1DIR)
        a2d.value(G_2DIR)
        a1s.value(0)
        a2s.value(0)
        sleep_ms(G_SPEED)
        a1s.value(1)
        a2s.value(1)
        sleep_ms(G_SPEED)

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
    c.subscribe(SPEED_TOPIC)
    c.check_msg()
    return c

def mqtt_callback(topic, msg):
    global G_SPEED, G_1DIR, G_2DIR
    print("Got callback: {} {}".format(topic, msg))
    if topic == SPEED_TOPIC:
        G_SPEED = int(str(bytearray(msg), "utf-8"))


def save_pattern(pattern):
    with open("pattern_"+str(pattern.id), 'w') as f:
        f.write(pattern.gcode)

def load_pattern(id):
    try:
        with open("pattern_"+str(id), 'r') as f:
            return pattern(id, f.read())
    except:
        return pattern(0,"G15 G1 X0 Y0")

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

