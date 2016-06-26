#!/usr/bin/env python3

import time
import serial
import sys
import struct
import random
from fire_pong.fp_event import FpEvent

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    #port='/dev/ttyACM0',
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
last = time.time()
time.sleep(1)
events = [ 
    FpEvent(0x1, 'FP_EVENT_RELAY', struct.pack('<H', 250)), 
    FpEvent(0x2, 'FP_EVENT_RELAY', struct.pack('<H', 250)),
    FpEvent(0x4, 'FP_EVENT_RELAY', struct.pack('<H', 250)),
    FpEvent(0x8, 'FP_EVENT_RELAY', struct.pack('<H', 250)),
    FpEvent(0x10, 'FP_EVENT_RELAY', struct.pack('<H', 250)),
    FpEvent(0x20, 'FP_EVENT_RELAY', struct.pack('<H', 250)),
    FpEvent(0x40, 'FP_EVENT_RELAY', struct.pack('<H', 250)),
    FpEvent(0x80, 'FP_EVENT_RELAY', struct.pack('<H', 250))
]

n=0
        
while 1:
    if ser.inWaiting() > 0:
        try:
            data = ser.read(1)
            sys.stdout.write(data.decode())
        except UnicodeDecodeError:
            sys.stdout.write('?')
    if time.time() - last > 0.15:
        last = time.time()
        e = events[n%len(events)]
        n+=1
        print('SEND:', str(e))
        ser.write(e.serialize())
        
