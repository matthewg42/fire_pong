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
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

last = time.time()
events = [ 
    #FpEvent(0x00010001, 'FP_EVENT_RESET'),
    #FpEvent(0x00010010, 'FP_EVENT_SPARK', struct.pack('<H', 100)),
    #FpEvent(0x00010010, 'FP_EVENT_DISPLAY', b'Game over'),
    FpEvent(0x00000001, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000002, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000003, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000004, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000005, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000006, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000007, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000008, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x00000009, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x0000000a, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x0000000b, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x0000000c, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x0000000d, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x0000000e, 'FP_EVENT_PUFF', struct.pack('<H', 100)),
    FpEvent(0x0000000f, 'FP_EVENT_PUFF', struct.pack('<H', 100))
]

time.sleep(1)
        
while 1:
    if ser.inWaiting() > 0:
        data = ser.read(1)
        sys.stdout.write(data.decode())
    if time.time() - last > 1.0:
        last = time.time()
        e = events[random.randint(0,len(events)-1)]
        ser.write(e.serialize())
        
