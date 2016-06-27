
from fire_pong.scoreboard import ScoreBoard
from fire_pong.fp_event import FpEvent
import logging
import time

log = logging

class PongMatch:
    def __init__(self, config, serial):
        self.reset()
        self.serial = serial
        self.config = config
        self.scoreboard = ScoreBoard(config, self.serial)
        self.running = True
        
    def reset(self):
        self.game = None
        self.scores = (0, 0)
        self.state = PongMatch.MATCH_START

    def do_io(self):
        # check GPIO pins, set HALT state if emergency stop pressed etc.
        pass

    def tick(self):
        self.do_io()
        if self.state == PongMatch.HALT:
            self.scoreboard.display('HALT')
            # TODO
            pass
        if self.state == PongMatch.MATCH_START:
            self.scoreboard.display('PONG')
        # TODO
        elif self.state == PongMatch.MATCH_END:
            self.scoreboard.display('%-2d%2d' % self.scores)
        elif self.state == PongMatch.MATCH_QUIT:
            self.scoreboard.display('bye!')
            self.running = False

    def shutdown(self):
        self.state = PongMatch.MATCH_QUIT

    def run(self):
        log.debug('PongMatch: start')
        while self.running:
            print('state=%s' % self.state)
            self.tick()
            time.sleep(1)
        log.debug('PongMatch: end')
            
    HALT = 0
    MATCH_START = 1
    MATCH_GAME_ACTIVE = 2
    MATCH_SCORE = 3
    MATCH_END = 4
    MATCH_QUIT = 5

