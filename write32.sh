#!/bin/bash
PORT="/dev/ttyUSB0"
errors=$(python3 -m pylint -E sand_drawing.py stepper.py cnc.py)
if [ ! -z "$errors" ]; then
  echo Problems in script. Fix them:
  echo "$errors"
  exit 1
fi
ampy -p "$PORT" put generator_libs.py
sleep 2
ampy -p "$PORT" put constants.py
sleep 2
ampy -p "$PORT" put sand_drawing.py
sleep 2
ampy -p "$PORT" put cnc.py
sleep 2
ampy -p "$PORT" put stepper.py
sleep 2
# exit 0
ampy -p "$PORT" put secrets.py
sleep 2
ampy -p "$PORT" put secrets_real.py
sleep 2
ampy -p "$PORT" put boot.py
sleep 2
# ./putty32.sh
