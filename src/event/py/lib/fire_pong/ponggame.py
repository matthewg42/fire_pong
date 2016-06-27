
import random
import logging
import time

log = logging

class PongGame:
    def __init__(self, config, serial):
        self.config = config
        self.serial = serial

    def run(self):
        log.debug('PongGame.run() playing game...')
        time.sleep(2)
        return (random.randint(0,10)%2)
