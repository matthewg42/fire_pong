""" Input manager class
    Runs a thread which monitors the state of the system's various
    inputs, and calls callbacks when those inputs are triggered.

    Also provides a set of functions to directly interrogate the
    state of the inputs
"""

import threading
import time
import logging
import traceback
import sys
import fire_pong.swipemote

from fire_pong.keyboard import Keyboard
from fire_pong.swipemote import SwipeMote
from fire_pong.util import tid
from fire_pong.events import *

log = logging

# Follows the singleton pattern
class InputManager:
    class __InputManager:
        def __init__(self, config):
            self.thread = threading.Thread(target=self.run)
            self.config = config
            self.terminate = False

            # Config wiimotes
            self.wm1 = None
            self.wm2 = None
            try:
                if config['InputManager']['wiimotes']['enabled']:
                    SwipeMote.IDLE = self.config['InputManager']['wiimotes']['swipe_idle']
                    SwipeMote.SWIPE_MIN = self.config['InputManager']['wiimotes']['swipe_min']
                    self.wm1 = SwipeMote('1UP', self.wiiswipe)
                    self.wm2 = SwipeMote('2UP', self.wiiswipe)
            except KeyError as e:
                log.exception('InputManager.__init__(): %s' % e)

            # Configure keyboard input
            self.keyboard = None
            try:
                if config['InputManager']['keyboard']['enabled']:
                    self.keyboard = Keyboard(config)
                    self.keyboard.thread.start()
            except Exception as e:
                log.exception('InputManager.__init__(): %s' % e)
                
            self.event_handler = None

        def discover(self):
            return
            if self.wm1 is None:
                self.wm1 = SwipeMote('1UP', self.wiiswipe)
                self.wm1.discover()

        def run(self):
            last_second = time.time()
            try:
                log.debug('InputManager[%s]: start' % tid())
                self.discover()
                while not self.terminate:
                    #log.debug('InputManager[%s]: tick' % tid())
                    t = time.time()

                    if self.wm1:
                        self.wm1.tick()
                    if self.wm2:
                        self.wm2.tick()

                    if self.keyboard:
                        if self.keyboard.get_start():
                            self.emit(EventButton('start'))
                        if self.keyboard.get_emstop():
                            self.emit(EventButton('emstop'))
                        if self.keyboard.get_back():
                            self.emit(EventButton('back'))
                        if self.keyboard.get_quit():
                            self.emit(EventQuit())

                    time.sleep(self.config['InputManager']['tick'])
                        
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                log.exception('InputManager[%s]: uncaught exception: %s, SHUTTING DOWN\n%s' % (tid(), e, repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
            log.debug('InputManager[%s]: end' % tid())

        def shutdown(self):
            log.debug('InputManager[%s]: shutdown() requested' % tid())
            if self.keyboard:
                self.keyboard.shutdown()
                self.keyboard.thread.join()
            self.terminate = True

        def emit(self, event):
            if self.event_handler is not None:
                self.event_handler(event)

        def set_event_handler(self, handler):
            # TODO: check it's a function!
            self.event_handler = handler

        def wiiswipe(self, player_id, swipe_strength):
            log.info('InputManager[%s]: wiiswipe(%s, %s)' % (tid(), player_id, swipe_strength))
            self.emit(EventSwipe(player_id, swipe_strength))
            self.swipes += 1
            if self.swipes == 3:
                self.shutdown()

    instance = None

    def __init__(self, config={'InputManager': {'tick': 0.02}}):
        if not InputManager.instance:
            InputManager.instance = InputManager.__InputManager(config)

    def __getattr__(self, name):
        return getattr(self.instance, name)

if __name__ == '__main__':
    def sh(signum, frame):
        global im
        log.INFO('caught signal, shutting down')
        im.shutdown()

    def eh(event):
        print('Got event: %-20s   is a swipe event: %s:' % (event, type(event) is EventSwipe))
        if type(event) is EventQuit:
            im.shutdown()

    import signal
    log.basicConfig(format='%(asctime)s %(name)s[%(process)d]' '%(levelname)s: %(message)s', level=logging.DEBUG)
    fire_pong.swipemote.log = log

    signal.signal(signal.SIGTERM, sh)

    config = {'InputManager': {'tick': 0.02, 'keyboard': { 'enabled': True, 'start': 's', 'emstop': 'h', 'back': 'b' }}}
    im = InputManager(config)
    im.set_event_handler(eh)
    im.thread.start()
    im.thread.join()
    log.info('all done')

