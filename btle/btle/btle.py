#!/usr/bin/env python

import struct
import logging
import bluepy.btle as btle
from bluepy.btle import Peripheral

btle.Debugging = True

log = logging

class BTLEButton(Peripheral):
    def __init__(self, addr):
        log.debug('connetion...')
        Peripheral.__init__(self, addr)
        log.debug('discovery...')
        self.discoverServices()
        self.notify_ch = None
        s = self.getServiceByUUID('fff0')
        self.cccd, = s.getCharacteristics('fff2')
        self.cccn, = s.getCharacteristics('fff1')
        log.debug('cccd: uuid=%s, commonName=%s, properties=%s' % (
            self.cccd.uuid,
            self.cccd.uuid.getCommonName(), 
            self.cccd.propertiesToString()))
        log.debug('cccn: uuid=%s, commonName=%s, properties=%s' % (
            self.cccn.uuid,
            self.cccn.uuid.getCommonName(), 
            self.cccn.propertiesToString()))
        self.cccd.write(b'\x01\x00')
        self.cccn.write(b'\x01\x00')

    def __del__(self):
        log.debug('disconnecting...')
        self.disconnect()

    def waitNotify(self):
        while True:
            print(self.waitForNotifications(1.0))

    def handler(handle, data):
        log.info('handler(handle=%s, data=%s)' % (repr(handle), repr(data)))

if __name__ == '__main__':
    import time
    log.basicConfig(level=logging.DEBUG)

    but = BTLEButton('18:7A:93:02:7C:5E')
    but.waitNotify()
    #cBTLEButton.ctrl.write(struct.pack('B', 0xff))
    #cBTLEButton.ctrl.write(struct.pack('B', 0))
    
    #while True:
    #    print(cBTLEButton.data.read())
    #    print(cBTLEButton.data.write('%s\n\r'%str(time.time())))
    #    time.sleep(1.0)
