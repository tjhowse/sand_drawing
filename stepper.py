# pylint: disable=E0401
from constants import *
from utime import ticks_us, ticks_diff
import machine

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

    def __init__(self, s_pin, d_pin, o_pin, debug=False, name='', home_index=0):
        self.s = machine.Pin(s_pin, machine.Pin.OUT)
        self.d = machine.Pin(d_pin, machine.Pin.OUT)
        # This is declared an output so we can use the internal pull-up.
        self.o = machine.Pin(o_pin, machine.Pin.OUT)
        self.o.value(1)
        self.set_dir(0)
        self.debug = debug
        self.name = name
        self.home_index = home_index

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
        angle %= 360
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
                self.index = self.home_index
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
        # if self.debug: print("Index: {}".format(self.index))
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
            # if self.debug: print("Prev Err: {} Err: {}".format(self.prev_err,err))
            self.prev_err = err


        return done_flag