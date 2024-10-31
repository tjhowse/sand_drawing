#!/bin/bash
# python3 -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 115200 write_flash -z 0x1000 ./esp32-idf3-20191220-v1.12.bin
python3 -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 115200 write_flash -z 0x1000 ./ESP32_GENERIC-20230426-v1.20.0.bin
#python3 -m esptool --port /dev/ttyS11 --baud 115200 write_flash --flash_size=detect -fm dout 0 ./esp32-idf3-20191220-v1.12.bin
