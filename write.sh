#!/bin/bash

# tty="/dev/ttyS16"
tty="/dev/ttyUSB0"
errors=$(python3 -m pylint -E sand_drawing.py)
# if [ ! -z "$errors" ]; then
#   echo Problems in script. Fix them:
#   echo "$errors"
#   exit 1
# fi
ampy -p "$tty" put constants.py
ampy -p "$tty" put cnc.py
ampy -p "$tty" put stepper.py
ampy -p "$tty" put generator_libs.py
ampy -p "$tty" put secrets.py
ampy -p "$tty" put secrets_real.py
ampy -p "$tty" put sand_drawing.py

ampy -p "$tty" put boot.py
