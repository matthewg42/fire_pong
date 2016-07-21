#!/usr/bin/env python2

import struct
from textwrap import wrap
from bluepy.btle import Peripheral, UUID
import bluepy.btle as btle

btle.Debugging = True

global ledev, addr
addr = '18:7A:93:03:A3:B8' 
ledev = None

def service(uuid):
    global ledev
    for u, s in ledev.services.items():
        print('%s : %s' % (str(u), str(s)))
        if u == uuid:
            print('Found %s' % uuid)
            return s
    print('%s not found' % uuid)
    return None

def handler(h, d):
    print('handler(h, d), h=%s, d=%s' % (repr(h), repr(d)))

ledev = Peripheral(addr)
ledev.discoverServices()
print('device:', ledev)
#for uuid in ['fff0', 'fff3']:
#    s = service(uuid)
#    for h in range(s.hndStart, s.hndEnd+1):
#        ledev.writeCharacteristic(h, struct.pack('<BB', 0, 1))

s = service('fff0')

print('listening for notifications...')
while True:
    print(ledev.waitForNotifications(1.))


