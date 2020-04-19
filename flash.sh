#!/bin/bash
python3 -m esptool --port /dev/ttyS16 --baud 115200 write_flash --flash_size=detect -fm dout 0 ./esp8266-20190529-v1.11.bin
