# pylint: disable=E0401

from umqtt.simple import MQTTClient
import time
from utime import ticks_us, ticks_ms, sleep_ms, sleep_us, ticks_diff
import machine
import network
import secrets
if secrets.wifi_ssid == 'my_ssid':
    import secrets_real as secrets

MICROCONTROLLER = "atom"
PWM_STEPPING = False
if MICROCONTROLLER == "d1mini":
    A1S_PIN = 16
    A1D_PIN = 5
    A2S_PIN = 4
    A2D_PIN = 0
    A1O_PIN = 12
    A2O_PIN = 14
elif MICROCONTROLLER == "atom":
    A1S_PIN = 33
    A1D_PIN = 23
    A2S_PIN = 19
    A2D_PIN = 22
    A1O_PIN = 21
    A2O_PIN = 25


MQTT_ENABLED = False

WIFI_CONNECT_WAIT_MAX_S = 10

SAND_DRAWING_TOPIC = secrets.mqtt_root+"/sand_drawing"
PATTERN_TOPIC = bytes(SAND_DRAWING_TOPIC+"/pattern", "utf-8")

G_PATTERN = ""

STEPS_PER_REV = 200
WILD_MODE = False
if WILD_MODE:
    MICROSTEPPING = 1
    DEFAULT_MOVE_SPEED = 180
else:
    MICROSTEPPING = 32
    DEFAULT_MOVE_SPEED = 180

GEAR_RATIO = 44/20
REAL_STEPS_PER_REV = int(STEPS_PER_REV*MICROSTEPPING*GEAR_RATIO)
REAL_STEPS_PER_DEGREE = REAL_STEPS_PER_REV/360
HALF_REAL_STEPS_PER_REV = REAL_STEPS_PER_REV/2

INDEX_CLOSE_ENOUGH = 3
HOME_SPEED = 180
NEW_PATTERN_CHECK_INTERVAL_MS = 2000


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

class cnc():
    # Coordinate modes:
    #   0: raw:        Default mode. Raw deg/second speed or degrees for each stepper. X is shaft 1, Y is shaft 2
    #   1: cartesian:  X is horizontal, Y is vertical.
    #   2: polar:      X is angle, Y is distance from centre.

    move_mode = 0
    coord_mode = 0
    debug = True
    gcode = None

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def set_pattern(self, new_pattern):
        print(new_pattern)
        self.pattern = new_pattern
        self.pattern_step = 0

    def set_gcode(self, gcode):
        self.gcode = gcode.split(' ')
        if self.debug:
            print(self.gcode)
        if self.gcode[0] == "G28":
            self.s1.set_speed(0)
            self.s2.set_speed(0)
            if len(self.gcode) == 1:
                return
            if self.gcode[1] == 'Y':
                if self.debug:
                    print("Homing Y axis")
                self.s2.home()
            elif self.gcode[1] == 'X':
                if self.debug:
                    print("Homing X axis")
                self.s1.home()
            return

        elif self.gcode[0] in ["G0", "G1"]:
            pwm_move = self.gcode[0] == "G0"
            if len(self.gcode) == 1:
                return
            for coord in self.gcode[1:]:
                if self.coord_mode == 0:
                    if self.move_mode == 0:
                        # Continuous raw movement
                        if coord.startswith('X'):
                            self.s1.set_speed(float(coord[1:]), pwm_motion=pwm_move)
                        elif coord.startswith('Y'):
                            self.s2.set_speed(float(coord[1:]), pwm_motion=pwm_move)
                    elif self.move_mode == 1:
                        # Discrete raw movement
                        if coord.startswith('X'):
                            self.s1.set_angle(float(coord[1:]), pwm_motion=pwm_move)
                        elif coord.startswith('Y'):
                            self.s2.set_angle(float(coord[1:]), pwm_motion=pwm_move)
                        elif coord.startswith('S'):
                            # This is where the speed of the movement is set.
                            pass

            return
        elif self.gcode[0] == "G15":
            # Set coordinate mode
            if len(self.gcode) == 1:
                return
            self.coord_mode = int(self.gcode[1])
            return
        elif self.gcode[0] == "G16":
            # Set movement mode
            if len(self.gcode) == 1:
                return
            self.move_mode = int(self.gcode[1])
            return
        elif self.gcode[0] == "J0":
            # Jump to a line in the gcode pattern
            step = int(self.gcode[1])
            if 0 <= step < len(self.pattern):
                self.pattern_step = step
                self.set_gcode(self.pattern[self.pattern_step])

    def tick(self):
        ticks = ticks_us()
        # Shortcut lazy-evaluation
        done1 = self.s1.go(ticks)
        done2 = self.s2.go(ticks)
        done = done1 and done2
        # Not very happy about this. Revisit it.
        if self.gcode and self.gcode[0] == "G28" and done:
            self.s1.homing = False
            self.s2.homing = False
        if done:
            self.pattern_step += 1
            if self.pattern_step < len(self.pattern):
                self.set_gcode(self.pattern[self.pattern_step])
            elif self.gcode != None:
                print("Done running pattern")
                self.gcode = None


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
    debug = True
    seeking = False # Moving towards target_index
    target_index = -1
    pwm = None
    prev_err = 0

    def __init__(self, s_pin, d_pin, o_pin, debug=False, name=''):
        self.s = machine.Pin(s_pin, machine.Pin.OUT)
        self.d = machine.Pin(d_pin, machine.Pin.OUT)
        # This is declared an output so we can use the internal pull-up.
        self.o = machine.Pin(o_pin, machine.Pin.OUT)
        self.o.value(1)
        self.set_dir(0)
        self.debug = debug
        self.name = name

    def set_speed(self, new_speed, pwm_motion=False):
        # Sets the speed in degrees per second
        if pwm_motion:
            if self.pwm == None:
                self.pwm = machine.PWM(self.s)
        else:
            if self.pwm != None:
                self.pwm.deinit()
            self.pwm = None
        if new_speed == 0:
            if self.pwm:
                self.pwm.duty(0)
            self.stepping = False
            self.seeking = False
        else:
            if new_speed < 0:
                self.set_dir(1)
            else:
                self.set_dir(0)
            self.stepping = True
            # Int for speed of calculation inside the tight loop fite me.
            self.step_interval = int(1e6*(1/(abs(new_speed)*REAL_STEPS_PER_DEGREE))/2)
            self.move_start_ticks_us = ticks_us()
            self.move_start_index = self.index
            if self.pwm != None:
                self.freq = int(abs(new_speed)*REAL_STEPS_PER_DEGREE)
                self.pwm.freq(self.freq)
                self.pwm.duty(int(self.freq/2))

        if self.debug:
            if self.name: print("Name: {}".format(self.name))
            print("New speed: {}".format(new_speed))
            print("step_interval: {}".format(self.step_interval))
            print("Stepping: {}".format(self.stepping))
            print("homing: {}".format(self.homing))
            print("homed: {}".format(self.homed))
            print("seeking: {}".format(self.seeking))
            print("Index: {}".format(self.index))
            print("target index: {}".format(self.target_index))
            if self.pwm != None:
                print("Freq: {}".format(self.freq))
            print("--------------------")

    def set_dir(self, new_dir):
        self.dir = new_dir
        self.d.value(1-self.dir)

    def set_angle(self, angle, speed=DEFAULT_MOVE_SPEED, pwm_motion=False):
        if not self.homed:
            print("Cannot set angle. Not homed.")
            return
        self.target_index = int(angle*REAL_STEPS_PER_DEGREE)
        diff = self.target_index - self.index
        if self.debug:
            print("Set angle: {}".format(angle))
            print("Index diff: {}".format(diff))
        if abs(diff) < INDEX_CLOSE_ENOUGH:
            self.set_speed(0)
            return
        else:
            self.seeking = True
        # If you can think of a cleaner, more readable version of this please let me know.
        if abs(diff) < REAL_STEPS_PER_REV/2:
            # Going straight there is faster.
            if diff < 0:
                self.set_speed(-speed, pwm_motion=pwm_motion)
            else:
                self.set_speed(speed, pwm_motion=pwm_motion)
        else:
            # Cross zero to get there
            if diff > 0:
                self.set_speed(-speed, pwm_motion=pwm_motion)
            else:
                self.set_speed(speed, pwm_motion=pwm_motion)

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
        # if self.debug: print(ticks_diff(ticks, self.last_step))
        self.high_low = 1 - self.high_low
        last_step_ticks_us = self.last_step
        self.last_step = ticks
        if self.pwm == None:
            self.s.value(self.high_low)
            if not self.high_low:
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
        if not self.homed:
            return done_flag
        # On a rising edge increase the index by 1 if going clockwise,
        # or decrement by 1 if going anti-clockwise.
        delta_index = 0
        if self.pwm == None:
            self.index += 1 + self.dir*-2
        else:
            # We have to update the index based on the amount of time elapsed since
            # the start of this movement and the speed of the movement. Eugh, a bit.
            # Slow float maths, but in PWM mode it doesn't matter too much.
            delta_index = int(self.freq * (ticks_diff(ticks, last_step_ticks_us)/1e6) * (1 + self.dir*-2))
            if self.debug: print("delta_index: {}".format(delta_index))
            self.index += delta_index
        self.index %= REAL_STEPS_PER_REV
        if self.debug: print("Index: {}".format(self.index))
        if self.pwm == None:
            if self.target_index == self.index:
                self.set_speed(0)
                done_flag = True
        else:
            err = int(HALF_REAL_STEPS_PER_REV - abs(abs(self.index - self.target_index) - HALF_REAL_STEPS_PER_REV))
            # If the error is smaller than a step, or if the error is increasing, stop.
            if err < abs(delta_index/2) or (self.prev_err < err):
                if self.debug: print("Stopping move")
                self.set_speed(0)
                done_flag = True
                self.prev_err = REAL_STEPS_PER_REV
            if self.debug: print("Prev Err: {} Err: {}".format(self.prev_err,err))
            self.prev_err = err


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

