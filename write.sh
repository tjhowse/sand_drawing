#!/bin/bash
errors=$(python3 -m pylint -E sand_drawing.py)
if [ ! -z "$errors" ]; then
  echo Problems in script. Fix them:
  echo "$errors"
  exit 1
fi
ampy -p /dev/ttyS16 put secrets.py
ampy -p /dev/ttyS16 put secrets_real.py
ampy -p /dev/ttyS16 put sand_drawing.py

ampy -p /dev/ttyS16 put boot.py
