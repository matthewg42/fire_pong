""" Keeps track of modes, and redirects events to the current mode
"""

import threading
import time
import logging
import traceback
import sys
import signal
import os

from fire_pong.util import tid
from fire_pong.inputmanager import InputManager
from fire_pong.mode import DebugEventsMode
from fire_pong.events import *

log = logging

class ModeManager:
    class __ModeManager:
        def __init__(self, start_mode, config):
            self.config = config
            try:
                float(self.config['ModeManager']['tick'])
            except Exception as e:
                raise Exception("could not find config item ModeManager.tick: %s" % type(e))
            self.thread = threading.Thread(target=self.run)
            self.terminate = False
            self.mode = []
            self.start_mode = start_mode
            self.event_handler = None
            InputManager().set_event_handler(self.dispatcher)

        def run(self):
            log.debug('ModeManager.run() start mode: %s' % self.start_mode)
            self.push_mode(self.start_mode)
            log.debug('ModeManager.run() end')

        def push_mode(self, mode):
            """ returns False of the caller should abort immediately """
            log.debug('ModeManager.push_mode(%s)' % mode)
            self.event_handler = mode.event
            self.mode.append(mode)
            ret = self.mode[-1].run()
            self.pop_mode()
            if self.terminate:
                return None
            elif ret is None:
                return True
            else:
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
            if type(event) is EventQuit:
                self.shutdown()

            if propagate and self.event_handler:
                log.debug('ModeManager.dispatcher propagating to %s' % self.event_handler)
                self.event_handler(event)

        def shutdown(self):
            log.debug('ModeManager.shutdown()')
            self.terminate = True

    instance = None
    def __init__(self, start_mode=DebugEventsMode(), config={'ModeManager': {'tick': 1}}):
        if not ModeManager.instance:
            ModeManager.instance = ModeManager.__ModeManager(start_mode, config)
   
    def __getattr__(self, name):
        return getattr(self.instance, name) 
        
if __name__ == '__main__':
    from fire_pong.events import *
    from fire_pong.mode import Mode
    import fire_pong.mode

    class InnerMode(Mode):
        def __init__(self, config={}, duration=3):
            Mode.__init__(self, config)
            self.duration = duration
            
        def run(self):
            log.info('InnerMode.run()')
            while not self.terminate and self.duration > 0:
                log.info('InnerMode.run() waiting %d...' % self.duration)
                self.duration -= 1
                time.sleep(1)
            log.info('InnerMode.end()')

        def event(self, event):
            log.debug('InnerMode: %s' % event)

    class OuterMode(Mode):
        def __init__(self, config={}):
            Mode.__init__(self, config)

        def run(self):
            log.info('OuterMode.run()')
            for i in range(0,2):
                log.info('OuterMode.run() waiting...')
                time.sleep(1)
            log.info('OuterMode.run() pushing InnerMode...')
            inner = InnerMode(3)
            if ModeManager().push_mode(inner) is None:
                return
            for i in range(0,2):
                log.info('OuterMode.run() waiting...')
                time.sleep(1)
            log.info('OuterMode.run() ending...')

        def event(self, event):
            log.debug('OuterMode: %s' % event)


    log.basicConfig(format='%(asctime)s %(name)s[%(process)d]' '%(levelname)s: %(message)s', level=logging.DEBUG)
    fire_pong.mode.log = log
    ModeManager(start_mode=OuterMode())
    ModeManager().thread.start()
    for i in range(0,20):
        InputManager().emit(EventMessage('pewp %d' % i))
        time.sleep(0.5)
    log.info('all done')

