#!/usr/bin/env python3

from fire_pong.fp_event import FpEvent
from fire_pong.crc8 import crc8
import struct
import sys

for e in [ FpEvent(1, 'FP_EVENT_HALT'),
           FpEvent(0x87654321, 'FP_EVENT_PUFF', struct.pack('<H', 1234))
         ]:
    print(str(e))
    print(e.serialize(), "\n")

buf = bytearray()
for b in ['f', 'P', 15, 1, 0, 0, 0, FpEvent.get_type_id('FP_EVENT_SPARK'), 'd', 'a', 't', 'a', 0x8a, 'f', 'P']:
    if type(b) is str:
        buf.append(ord(b))
    else:
        buf.append(b)
e = FpEvent.from_bytes(buf)
print(str(e))

# corrupt it so the cksum is bad
buf[8] = ord('D')
e = FpEvent.from_bytes(buf)
print(str(e))


