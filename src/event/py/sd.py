#!/usr/bin/env python3

import time
import serial
import sys
import struct

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

while 1:
    if ser.inWaiting() > 0:
        data = ser.read(1)
        sys.stdout.write(data.decode())


