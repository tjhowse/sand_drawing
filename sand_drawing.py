# pylint: disable=E0401

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
WILD_MODE = True
if WILD_MODE:
    MICROSTEPPING = 1
    DEFAULT_MOVE_SPEED = 180
else:
    MICROSTEPPING = 16
    DEFAULT_MOVE_SPEED = 360

GEAR_RATIO = 44/20
STEPS_PER_DEGREE = (STEPS_PER_REV*MICROSTEPPING*GEAR_RATIO)/360

CLOSE_ENOUGH_ANGLE = 1
HOME_SPEED = DEFAULT_MOVE_SPEED

def main():
    s1 = stepper(A1S_PIN, A1D_PIN, A1O_PIN)
    s2 = stepper(A2S_PIN, A2D_PIN, A2O_PIN)
    my_cnc = cnc(s1, s2)

    # pattern = ["G28 X", "G28 Y", "G1 X-180 Y360"]
    pattern = [ "G28 X",
                "G28 Y",
                "G16 1",
                "G1 X90 Y0",
                "G1 Y180",
                "G1 Y270",
                "G1 Y360",
                "G1 X180 Y90",
                "G1 Y180",
                "G1 Y270",
                "G1 Y360",
                "G1 X270 Y180",
                "G1 Y180",
                "G1 Y270",
                ]
    pattern_step = 0

    while True:
        my_cnc.gcode(pattern[pattern_step])
        while not my_cnc.tick():
            pass
        pattern_step += 1
        if pattern_step == len(pattern):
            # We're done!
            print("Done")
            pattern_step = 0
            # while True:
                # sleep_ms(1000)


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

class cnc():
    # Coordinate modes:
    #   0: raw:        Default mode. Raw deg/second speed or degrees for each stepper. X is shaft 1, Y is shaft 2
    #   1: cartesian:  X is horizontal, Y is vertical.
    #   2: polar:      X is angle, Y is distance from centre.

    move_mode = 0
    coord_mode = 0
    debug = False

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def gcode(self, gcode):
        self.code = gcode.split(' ')
        if self.debug:
            print(self.code)
        if self.code[0] == "G28":
            self.s1.set_speed(0)
            self.s2.set_speed(0)
            if len(self.code) == 1:
                return
            if self.code[1] == 'Y':
                if self.debug:
                    print("Homing Y axis")
                self.s2.home()
            elif self.code[1] == 'X':
                if self.debug:
                    print("Homing X axis")
                self.s1.home()
            return

        elif self.code[0] == "G1":
            if len(self.code) == 1:
                return
            for coord in self.code[1:]:
                if self.coord_mode == 0:
                    if self.move_mode == 0:
                        # Continuous raw movement
                        if coord.startswith('X'):
                            self.s1.set_speed(float(coord[1:]))
                        elif coord.startswith('Y'):
                            self.s2.set_speed(float(coord[1:]))
                    elif self.move_mode == 1:
                        # Discrete raw movement
                        if coord.startswith('X'):
                            self.s1.set_angle(float(coord[1:]))
                        elif coord.startswith('Y'):
                            self.s2.set_angle(float(coord[1:]))
                        elif coord.startswith('S'):
                            # This is where the speed of the movement is set.
                            pass

            return
        elif self.code[0] == "G15":
            # Set coordinate mode
            if len(self.code) == 1:
                return
            self.coord_mode = int(self.code[1])
            return
        elif self.code[0] == "G16":
            # Set movement mode
            if len(self.code) == 1:
                return
            self.move_mode = int(self.code[1])
            return

    def tick(self):
        ticks = ticks_us()
        # Shortcut lazy-evaluation
        done1 = self.s1.go(ticks)
        done2 = self.s2.go(ticks)
        done = done1 and done2
        # Not very happy about this. Revisit it.
        if self.code[0] == "G28" and done:
            self.s1.homing = False
            self.s2.homing = False
        return done

class stepper():
    # This manages the interface to a stepper
    s = None # The step output Pin object
    d = None # The direction output Pin object
    o = None # The optoswitch input Pin object
    dir = 0 # 0: Clockwise, 1: Counterclockwise
    step_interval = 0 # The number of ticks_us between rising or falling edges of the step pin
    last_step = 0 # The last ticks_us of a rising or falling edge
    index = -1 # 0-x the number of steps
    last_o = 1 # Used for detecting the rising edge of the opto pin
    high_low = 0 # The state of the step pin. 0: low, 1: high
    homing = True
    homed = False
    stepping = True
    debug = False
    seeking = False # Moving towards target_angle
    target_angle = -1

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
        if new_speed < 0:
            new_speed *= -1
            self.set_dir(1)
        else:
            self.set_dir(0)
        self.stepping = True
        self.step_interval = 1e6*(1/(new_speed*STEPS_PER_DEGREE))/2
        if self.debug:
            print("New speed: {}".format(new_speed))
            print("Stepping: {}".format(self.stepping))
            print("homing: {}".format(self.homing))
            print("homed: {}".format(self.homed))

    def set_dir(self, new_dir):
        self.dir = new_dir
        self.d.value(1-self.dir)

    def set_angle(self, angle, speed = DEFAULT_MOVE_SPEED):
        if not self.homed:
            return
        # TODO set the speed such that it turns the shortest direction to the target.

        if self.debug:
            print("Set angle: {}".format(angle))
        self.target_angle = angle
        self.seeking = True
        self.set_speed(speed)

    def home(self):
        self.homed = False
        self.homing = True
        self.set_speed(HOME_SPEED)

    def go(self, ticks):
        done_flag = False
        if not self.stepping:
            return True
        if ticks_diff(ticks, self.last_step) <= self.step_interval:
            return False
        if self.homing:
            if self.last_o == 0 and self.o.value() == 1 and self.dir == 0:
                # Rising edge opto when rotating clockwise. We're at zero.
                self.homed = True
                self.index = 0
                self.set_speed(0)
                if self.debug:
                    print("homed")
                return True
            elif self.homed:
                done_flag = True
                return True
            self.last_o = self.o.value()
        self.high_low = 1 - self.high_low
        self.s.value(self.high_low)
        self.last_step = ticks
        if self.homed and self.high_low == 1:
            # On a rising edge increase the index by 1 if going clockwise,
            # or decrement by 1 if going anti-clockwise.
            self.index += 1 + self.dir*-2
        if self.index < 0:
            # TODO Eugh oh gross.
            self.index = int((360 * STEPS_PER_DEGREE) - 1/STEPS_PER_DEGREE)
        if self.index >= 360*STEPS_PER_DEGREE:
            self.index = 0
        if self.seeking and self.homed:
            if abs(self.index/STEPS_PER_DEGREE-self.target_angle) < CLOSE_ENOUGH_ANGLE:
                self.set_speed(0)
                done_flag = True
                self.seeking = False
        return done_flag

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

