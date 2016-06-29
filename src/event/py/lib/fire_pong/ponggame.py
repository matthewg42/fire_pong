
import random
import logging
import time

log = logging

class PongGame:
    def __init__(self, config, serial, wm1, wm2):
        self.config = config
        self.serial = serial

    def run(self):
        log.debug('PongGame.run() playing game...')
        time.sleep(2)
        return (random.randint(0,10)%2)

    HALT = 0
    COUNTDOWN = 1
    RUNNING_P1 = 2
    P1_HIT = 3
    P1_MISS = 4
    RUNNING_P2 = 5
    P2_HIT = 6
    P2_MISS = 7
    END_GAME = 8
    QUIT = 9
    
    
