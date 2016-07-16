import logging
import time
import threading
import struct
import fire_pong.util
from random import randint
from fire_pong.mode import Mode
from fire_pong.fp_event import FpEvent
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
from fire_pong.fp_serial import FpSerial
log = logging

def strength2delay(strength):
    d = 0.8 - (float(strength)/300)
    if d <= 0.2:
        d = 0.2
    return d

class PongMatch(Mode):
    def __init__(self):
        Mode.__init__(self)
        self.winning_score = fire_pong.util.config['PongMatch']['winning_score']
        self.start_player = randint(1, 2)

    def reset(self):
        log.info('PongMatch: NEW MATCH')
        self.score = [0,0]

    def display_score(self):
        ScoreBoard().display('%d%d' % tuple(self.score))

    def run(self):
        log.debug('PongMatch.run()')

        while not self.terminate:
            self.reset()
            while max(self.score) < self.winning_score and not self.terminate:
                self.display_score()
                if ModeManager().push_mode(PongWaitStart()) is None:
                    return
                if ModeManager().push_mode(CounterMode(start=3, end=1)) is None:
                    return
                self.display_score()
                win = ModeManager().push_mode(PongGame(self.start_player))
                if win is None:
                    self.terminate = True
                else:
                    self.score[win-1] += 1
                if self.start_player == 1:
                    self.start_player = 2
                else:
                    self.start_player = 1

            if self.score[0] > self.score[1]:
                log.info("Player 1 wins")
                ScoreBoard().display("1W")
            elif self.score[1] > self.score[0]:
                log.info("Player 2 wins")
                ScoreBoard().display("2W")
            else:
                log.info("It's a DRAW!")
                ScoreBoard().display("Dr")

        log.debug('PongMatch.run() ended')

    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class PongWaitStart(Mode):
    def __init__(self):
        Mode.__init__(self)

    def run(self):
        log.debug('PongWaitStart.run()')
        while not self.terminate:
            time.sleep(0.5)
        log.debug('PongWaitStart.run() ending')
        
    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class CounterMode(Mode):
    """ Designed for countdowns at the start of games """
    def __init__(self, start=3, end=1, time=1):
        Mode.__init__(self)
        self.count = start
        self.end = end
        if start > end:
            self.step = -1
        else:
            self.step = +1
        self.time = time

    def run(self):
        log.debug('CounterMode.run()')
        while not self.terminate and self.count != self.end + self.step:
            ScoreBoard().display(str(self.count))
            self.count += self.step
            time.sleep(self.time)
        log.debug('CounterMode.run() countdown ended')

    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class PongGame(Mode):
    def __init__(self, start_player):
        Mode.__init__(self)
        self.puffers = fire_pong.util.config['PongGame']['puffers']
        self.delay = fire_pong.util.config['PongGame']['initial_delay']
        self.puff_duration = fire_pong.util.config['PongGame']['puff_duration']
        self.hit_idx = {'1UP': [-1, 0], '2UP': [len(self.puffers)-1, len(self.puffers)]}
        self.win = None
        self.start_player = start_player
        if self.start_player == 1:
            self.idx = 0
            self.inc = 1
        else:
            self.idx = len(self.puffers)-1
            self.inc = -1

    def run(self):
        log.debug('PongGame.run()')
            
        while self.win is None:
            if self.terminate:
                return
            if self.idx < -1:
                self.win = 2
                break
            elif self.idx >= len(self.puffers)+1:
                self.win = 1
                break
            elif self.idx >= 0 and self.idx < len(self.puffers):
                d = ['', '', '']
                for i in range(0, len(self.puffers)):
                    d[0] += '   ' if i != self.idx else ' @ '
                    d[1] += '   ' if i != self.idx else ' @ '
                    d[2] += ' | ' if i != self.idx else ' | '
                for i in range(0,3):
                    print(d[i])
                log.info("PUFF idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
                e = FpEvent(self.puffers[self.idx], 'FP_EVENT_PUFF', struct.pack('<H', self.puff_duration))
                print(str(e))
                FpSerial().write(e.serialize())
            else:
                log.info('[relief]')
            self.idx += self.inc
            time.sleep(self.delay)
        return self.win
            
    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

        if type(event) is EventSwipe:
            log.debug('Swipe by %s' % event.player)
            if self.idx in self.hit_idx[event.player]:
                log.info("Player %s HITS!" % event.player)
                if event.player == '1UP':
                    self.inc = 1
                else:
                    self.inc = -1
                self.delay = strength2delay(event.strength)
            else:
                log.info('Player %s MISS!' % event.player)

if __name__ == '__main__':
    log.basicConfig(level=logging.DEBUG)
    m = CounterMode(start=1, end=5, time=0.3)
    m.thread.start()
    m.thread.join()


