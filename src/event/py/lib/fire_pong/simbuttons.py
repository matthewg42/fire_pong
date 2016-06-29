import abc
import os
import logging
from fire_pong.basebuttons import Buttons

log = logging

"""
    SimButtons - simulate GPIO buttons with the filesystem
    This is for use when testing not on an RPi.
"""
class SimButtons(Buttons):
    def __init__(self, config):
        for b in ['start','halt']:
            log.debug('SimButtons() %s file = %s' % (b, config['buttons']['simbuttons'][b]))
        self.config = config

    def getEmergencyStop(self):
        return os.path.exists(self.config['buttons']['simbuttons']['halt'])

    def getStartButton(self):
        return os.path.exists(self.config['buttons']['simbuttons']['start'])

if __name__ == '__main__':
    import time

    log.basicConfig(level=logging.DEBUG)

    config = { 'buttons': { 'simbuttons': { 'start': '/tmp/start', 'halt': '/tmp/halt' } } }
    b = SimButtons(config);
    while True:
        print("stop=%s start=%s" % (b.getEmergencyStop(), b.getStartButton()))
        time.sleep(0.5)
    
