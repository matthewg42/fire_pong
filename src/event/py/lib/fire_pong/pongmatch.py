
from fire_pong.scoreboard import ScoreBoard
from fire_pong.fp_event import FpEvent
from fire_pong.buttons import SimButtons
from fire_pong.ponggame import PongGame
import logging
import time

log = logging

class PongMatch:
    def __init__(self, config, serial):
        self.reset()
        self.serial = serial
        self.config = config
        self.winning_score = self.config['pongmatch']['winning_score']
        self.scoreboard = ScoreBoard(config, self.serial)
        self.buttons = SimButtons()
        self.running = True
        
    def reset(self):
        self.game = None
        self.scores = [0, 0]
        self.previous_state = PongMatch.MATCH_START
        self.update_state(PongMatch.MATCH_START, update_prev=False)

    def update_state(self, state, update_prev=True):
        if update_prev:
            self.previous_state = self.state
        self.state = state
        self.new_state = True

    def do_io(self):
        # check GPIO pins, set HALT state if emergency stop pressed etc.
        pass

    def shutdown(self):
        self.state = PongMatch.MATCH_QUIT

    def run(self):
        log.debug('PongMatch: start')
        while self.running:
            if self.state == PongMatch.HALT:
                if self.buttons.getStartButton():
                    self.update_state(PongMatch.MATCH_START)
                    next
                if self.new_state:
                    self.new_state = False
                    self.scoreboard.display('HALT')
                    next

            if self.state == PongMatch.MATCH_START:
                if self.buttons.getStartButton():
                    self.update_state(PongMatch.MATCH_GAME_ACTIVE)
                    next
                if self.new_state:
                    self.new_state = False
                    self.scoreboard.display('PONG')
                    next

            if self.state == PongMatch.MATCH_GAME_ACTIVE:
                game = PongGame(self.config, self.serial)
                winner = game.run()
                self.scores[winner] += 1
                if self.scores[winner] >= self.winning_score:
                    self.update_state(PongMatch.MATCH_END)
                else:
                    self.update_state(PongMatch.MATCH_SCORE)
                next
            
            if self.state == PongMatch.MATCH_SCORE:
                if self.new_state:
                    self.new_state = False
                    self.scoreboard.display('%-2d%2d' % (self.scores[0], self.scores[1]))
                    next
                if self.buttons.getStartButton():
                    self.update_state(PongMatch.MATCH_GAME_ACTIVE)
                    next

            if self.state == PongMatch.MATCH_END:
                if self.new_state:
                    self.new_state = False
                    self.scoreboard.display('WIN%d' % 1 if self.scores[0]>self.scores[1] else 0)
                    next
                if self.buttons.getStartButton():
                    self.reset()
                    next

            if self.state == PongMatch.MATCH_QUIT:
                self.scoreboard.display('bye!')
                self.running = False

            time.sleep(1)
        log.debug('PongMatch: end')
            
    HALT = 0
    MATCH_START = 1
    MATCH_GAME_ACTIVE = 2
    MATCH_SCORE = 3
    MATCH_END = 4
    MATCH_QUIT = 5

