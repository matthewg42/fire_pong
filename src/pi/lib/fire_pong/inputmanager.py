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
import fire_pong.util
from fire_pong.keyboard import Keyboard
from fire_pong.swipemote import SwipeMote
from fire_pong.util import tid
from fire_pong.events import *
from random import randint

log = logging

# Follows the singleton pattern
class InputManager:
    class __InputManager:
        def __init__(self):
            self.thread = threading.Thread(target=self.run)
            self.terminate = False

            # Config wiimotes
            self.wm1 = None
            self.wm2 = None
            try:
                if fire_pong.util.config['InputManager']['wiimotes']['enabled']:
                    SwipeMote.IDLE = fire_pong.util.config['InputManager']['wiimotes']['swipe_idle']
                    SwipeMote.SWIPE_MIN = fire_pong.util.config['InputManager']['wiimotes']['swipe_min']
                    self.wm1 = SwipeMote('1UP', self.wiiswipe)
                    self.wm2 = SwipeMote('2UP', self.wiiswipe)
                    self.discover()
            except KeyError as e:
                log.exception('InputManager.__init__(): %s' % e)

            # Configure keyboard input
            self.keyboard = None
            try:
                if fire_pong.util.config['InputManager']['keyboard']['enabled']:
                    self.keyboard = Keyboard()
                    self.keyboard.thread.start()
            except Exception as e:
                log.exception('InputManager.__init__(): %s' % e)
                
            self.event_handler = None

        def discover(self):
            if self.wm1 is not None:
                self.wm1.discover()
            if self.wm2 is not None:
                self.wm2.discover()

        def run(self):
            last_second = time.time()
            try:
                log.debug('InputManager[%s]: start' % tid())
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
                        if self.keyboard.get_swipe1():
                            self.emit(EventSwipe('1UP', randint(20, 300)))
                        if self.keyboard.get_swipe2():
                            self.emit(EventSwipe('2UP', randint(20, 300)))

                    time.sleep(fire_pong.util.config['InputManager']['tick'])
                        
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

        def wiiswipe(self, player, strength):
            log.info('InputManager[%s]: wiiswipe(%s, %s)' % (tid(), player, strength))
            self.emit(EventSwipe(player, strength))

    instance = None

    def __init__(self):
        if not InputManager.instance:
            InputManager.instance = InputManager.__InputManager()

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

    fire_pong.util.config = {
        'InputManager': {
            'tick': 0.02, 
            'keyboard': { 
                'tick': 0.02, 
                'enabled': True, 
                'start': 's', 
                'emstop': 'h', 
                'back': 'b', 
                'swipe1': 'z',
                'swipe2': 'COMMA'
            }
        }
    }
    im = InputManager()
    im.set_event_handler(eh)
    im.thread.start()
    im.thread.join()
    log.info('all done')

