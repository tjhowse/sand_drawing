#!/bin/bash
errors=$(python3 -m pylint -E sand_drawing.py stepper.py cnc.py)
if [ ! -z "$errors" ]; then
  echo Problems in script. Fix them:
  echo "$errors"
  exit 1
fi
ampy -p /dev/ttyS11 put generator_libs.py
sleep 2
ampy -p /dev/ttyS11 put constants.py
sleep 2
ampy -p /dev/ttyS11 put sand_drawing.py
sleep 2
ampy -p /dev/ttyS11 put cnc.py
sleep 2
ampy -p /dev/ttyS11 put stepper.py
sleep 2
# exit 0
ampy -p /dev/ttyS11 put secrets.py
sleep 2
ampy -p /dev/ttyS11 put secrets_real.py
sleep 2
ampy -p /dev/ttyS11 put boot.py
sleep 2
./putty32.sh
