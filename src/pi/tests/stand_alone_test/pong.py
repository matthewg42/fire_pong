#!/usr/bin/env python2

import sys
import logging
import struct
import time
from fp_serial import FpSerial
from fp_event import FpEvent


if __name__ == '__main__':
    log = logging
    log.basicConfig(level=logging.DEBUG)
    config = {
        "serial": {
            "port": "/dev/ttyUSB0",
            "baudrate": 115200,
            "parity": "none",
            "stopbits": 1,
            "bytesize": 8,
            "debug": True
        }
    }
    if len(sys.argv) == 2:
        config['serial']['port'] = sys.argv[1]

    fpserial = FpSerial(config)
    ids = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x100, 0x200, 0x400, 0x800]
    seq = ids
    seq.extend(list(reversed(ids[1:-1])))
    while True:
        for pid in seq:
            pic = "%12s" % "{0:b}".format(pid)
            pic = pic.replace('0', ' ')
            print(pic)
            e = FpEvent(pid, 'FP_EVENT_PUFF', struct.pack('<H', 100))
            log.debug(str(e))
            fpserial.write(e.serialize())
            time.sleep(0.3)


