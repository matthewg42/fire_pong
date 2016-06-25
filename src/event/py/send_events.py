#!/usr/bin/env python3

import time
import serial
import sys
import struct
import random
from fire_pong.fp_event import FpEvent

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

last = time.time()
events = [ 
    FpEvent(0xFFFFFFFF, 'FP_EVENT_HALT'),
    FpEvent(0x00010001, 'FP_EVENT_RESET'),
    FpEvent(0x00010010, 'FP_EVENT_SPARK', struct.pack('<H', 100)),
    FpEvent(0x00010010, 'FP_EVENT_DISPLAY', b'Game over')
]

time.sleep(1)
        
while 1:
    if ser.inWaiting() > 0:
        data = ser.read(1)
        sys.stdout.write(data.decode())
    if time.time() - last > 0.08:
        last = time.time()
        e = events[random.randint(0,len(events)-1)]
        ser.write(e.serialize())
        
