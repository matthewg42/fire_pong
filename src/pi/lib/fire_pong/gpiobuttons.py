import pygame
import threading
import time
import os
import wiringpi
import inspect

import fire_pong.util 
from fire_pong.util import log

# Follows the singleton pattern
class GpioButtons:
    class __GpioButtons:
        def __init__(self, callback):
            log.debug('GpioButtons.__init__')
            wiringpi.wiringPiSetupGpio()
            self.debounce = dict()
            self.debounce_time = fire_pong.util.config['InputManager']['gpio']['debounce_time']
            self.callback = callback
            for action in ['quit', 'start', 'swipe1', 'swipe2']:
                try:
                    pin = fire_pong.util.config['InputManager']['gpio'][action]
                    wiringpi.pinMode(pin, wiringpi.GPIO.INPUT)
                    wiringpi.pullUpDnControl(pin, wiringpi.GPIO.PUD_UP)
                    wiringpi.wiringPiISR(pin, wiringpi.GPIO.INT_EDGE_FALLING, getattr(self, action))
                    self.debounce[action] = 0
                    log.debug('GpioButtons.__init__() %s => pin %s' % (action, pin))
                    
                except KeyError as e:
                    log.warning('GpioButtons.__init__(): %s' % e)
                    pass

        def button(self, action):
            if time.time() - self.debounce[action] > self.debounce_time:
                self.callback(action)
                self.debounce[action] = time.time()

        def quit(self):
            self.button(str(inspect.stack()[0][3]))
            
        def start(self):
            self.button(str(inspect.stack()[0][3]))
            
        def swipe1(self):
            self.button(str(inspect.stack()[0][3]))
            
        def swipe2(self):
            self.button(str(inspect.stack()[0][3]))
            
    instance = None

    def __init__(self, callback):
        if not GpioButtons.instance:
            GpioButtons.instance = GpioButtons.__GpioButtons(callback)
        
    def __getattr__(self, name):
        return getattr(self.instance, name)

if __name__ == '__main__':
    import time
    import logging
    log = logging
    fire_pong.util.config = {
        "InputManager": {
            "tick": 0.02,
            "gpio": {
                "enabled": True,
                "quit": 6,
                "start": 13,
                "swipe1": 19,
                "swipe2": 26,
                "debounce_time": 0.20
            }
        }
    }

    def test_callback(action):
        print('test_callback got action: %s' % action)

    log.basicConfig(format='%(asctime)s %(name)s[%(process)d]' '%(levelname)s: %(message)s', level=logging.DEBUG)
    print('Waiting for button presses')
    k = GpioButtons(test_callback)
    while True:
        time.sleep(1)


