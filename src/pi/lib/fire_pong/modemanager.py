""" Keeps track of modes, and redirects events to the current mode
"""

import threading
import time
import traceback
import sys
import signal
import os
import fire_pong.util

from fire_pong.util import tid, log
from fire_pong.inputmanager import InputManager
from fire_pong.mode import DebugEventsMode
from fire_pong.events import *

class ModeManager:
    class __ModeManager:
        def __init__(self, start_mode):
            try:
                float(fire_pong.util.config['ModeManager']['tick'])
            except Exception as e:
                raise Exception("could not find config item ModeManager.tick: %s" % type(e))
            self.thread = threading.Thread(target=self.run)
            self.mode = []
            self.start_mode = start_mode
            self.event_handler = None
            InputManager().set_event_handler(self.dispatcher)

        def run(self):
            log.debug('ModeManager.run() START mode: %s' % self.start_mode)
            r = self.push_mode(self.start_mode)
            log.debug('ModeManager.run() END, (top level mode returned: %s)' % r)

        def push_mode(self, mode):
            log.debug('ModeManager.push_mode(%s)' % mode)
            self.event_handler = mode.event
            self.mode.append(mode)
            ret = self.mode[-1].run()
            self.pop_mode()
            return ret

        def pop_mode(self):
            self.mode.pop()
            try:
                self.event_handler = self.mode[-1].event
            except:
                self.event_handler = None

        def dispatcher(self, event):
            log.debug('ModeManager.dispatcher received: %s' % event)
            propagate = True
            if propagate and self.event_handler:
                log.debug('ModeManager.dispatcher propagating to %s' % self.event_handler)
                self.event_handler(event)

        def shutdown(self):
            log.debug('ModeManager.shutdown()')

    instance = None
    def __init__(self, start_mode=DebugEventsMode()):
        if not ModeManager.instance:
            ModeManager.instance = ModeManager.__ModeManager(start_mode)
   
    def __getattr__(self, name):
        return getattr(self.instance, name) 
        
if __name__ == '__main__':
    import logging
    log = logging
    log.basicConfig(level=logging.DEBUG)
