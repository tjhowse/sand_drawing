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
A1O_PIN = 12
A2O_PIN = 14

WIFI_CONNECT_WAIT_MAX_S = 10

SAND_DRAWING_TOPIC = secrets.mqtt_root+"/sand_drawing"
SPEED_TOPIC = SAND_DRAWING_TOPIC+"/speed"
A1DIR_TOPIC = SAND_DRAWING_TOPIC+"/1dir"
A2DIR_TOPIC = SAND_DRAWING_TOPIC+"/2dir"

G_SPEED = 1
G_1DIR = 1
G_2DIR = 1
STEPS_PER_REV = 200
MICROSTEPPING = 16
GEAR_RATIO = 44/20
STEPS_PER_DEGREE = (STEPS_PER_REV*MICROSTEPPING*GEAR_RATIO)/360

def main():
    s2 = stepper(A2S_PIN, A2D_PIN, A2O_PIN)
    s1 = stepper(A1S_PIN, A1D_PIN, A1O_PIN)
    s2.set_speed(360)
    s1.set_speed(360)

    while True:
        ticks = ticks_us()
        s2.go(ticks)
        s1.go(ticks)
        sleep_us(1)

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

class stepper():
    # This manages the interface to a stepper
    s = None # The step output Pin object
    d = None # The direction output Pin object
    o = None # The optoswitch input Pin object
    dir = 0 # 0: Clockwise, 1: Counterclockwise
    step_interval = 0 # The number of ticks_us between rising or falling edges of the step pin
    last_step = 0 # The last ticks_us of a rising or falling edge
    index = 0 # 0-199 the number of steps
    last_o = False # Used for detecting the rising edge of the opto pin
    high_low = 0 # The state of the step pin. 0: low, 1: high
    homing = True
    stepping = True

    def __init__(self, s_pin, d_pin, o_pin):
        self.s = machine.Pin(s_pin, machine.Pin.OUT)
        self.d = machine.Pin(d_pin, machine.Pin.OUT)
        # This is declared an output so we can use the internal pull-up.
        self.o = machine.Pin(o_pin, machine.Pin.OUT)
        self.o.value(1)
        self.set_dir(0)

    def set_speed(self, new_speed):
        # Sets the speed in degrees per second
        if new_speed == 0:
            self.stepping = False
            return
        self.stepping = True
        self.step_interval = 1e6*(1/(new_speed*STEPS_PER_DEGREE))/2

    def set_dir(self, new_dir):
        self.dir = new_dir
        self.d.value(1-self.dir)

    def go(self, ticks):
        if not self.stepping or ticks_diff(ticks, self.last_step) <= self.step_interval:
            return
        if self.homing:
            if self.last_o == 0 and self.o.value() == 1 and self.dir == 0:
                # Rising edge opto when rotating clockwise. We're at zero.
                self.homing = False
                self.index = 0
            self.last_o = self.o.value()
        self.high_low = 1 - self.high_low
        self.s.value(self.high_low)
        self.last_step = ticks
        if self.high_low == 1:
            # On a rising edge increase the index by 1 if going clockwise,
            # or decrement by 1 if going anti-clockwise.
            self.index += 1 + self.dir*-2


def do_step(speed, a1s, ):
    a1s.value(0)
    a2s.value(0)
    sleep_ms(speed)
    if on_1:
        a1s.value(1)
    if on_2:
        a2s.value(1)
    if a1d.value() != dir_1:
        a1d.value(dir_1)
    if a2d.value() != dir_2:
        a2d.value(dir_2)
    sleep_ms(speed)

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

