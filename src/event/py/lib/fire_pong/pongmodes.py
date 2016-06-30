import logging
import time
import threading
from random import randint
from fire_pong.mode import Mode
from fire_pong.fp_event import FpEvent
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
log = logging

class WaitStart(Mode):
    def __init__(self):
        Mode.__init__(self)

    def run(self):
        log.debug('WaitStart.run()')
        while not self.terminate:
            time.sleep(0.5)
        log.debug('WaitStart.run() ending')
        
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
            print('TODO: display event for count %d' % self.count)
            self.count += self.step
            time.sleep(self.time)
        log.debug('CounterMode.run() countdown ended')

    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class PongMatch(Mode):
    def __init__(self, config={}):
        Mode.__init__(self, config)
        self.winning_score = config['PongMatch']['winning_score']
        self.reset()

    def reset(self):
        print('PongMatch NEW MATCH')
        self.score = [0,0]

    def run(self):
        log.debug('PongMatch.run()')

        while not self.terminate:
            self.reset()
            #if ModeManager().push_mode(WaitStart()) is None:
            #    return
            while max(self.score) < self.winning_score and not self.terminate:
                if ModeManager().push_mode(CounterMode(start=3, end=1)) is None:
                    return
                win = ModeManager().push_mode(PongGame(self.config))
                if win is None:
                    self.terminate = True
                else:
                    self.score[win] += 1

            if self.score[0] > self.score[1]:
                print("Player 1 wins")
            elif self.score[1] > self.score[0]:
                print("Player 2 wins")
            else:
                print("It's a DRAW!")

        log.debug('PongMatch.run() ended')

    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class PongGame(Mode):
    def __init__(self, config):
        Mode.__init__(self, config)

    def run(self):
        log.debug('PongGame.run()')
        seqs = [P1Seq(self.config), P2Seq(self.config)]
        idx = randint(0,1)
        while not self.terminate:
            if ModeManager().push_mode(seqs[idx%2]) is None:
                return
            if randint(1, 3) == 1:
                break
            idx += 1
        winner = idx%2
        print('GAME OVER with winner = %d' % winner)
        log.debug('PongGame.run() ending')
        return winner
        
    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class P1Seq(Mode):
    def __init__(self, config):
        Mode.__init__(self, config)
        self.puffers = config['small_puffers']['ids']

    def run(self):
        log.debug('P1Seq.run()')
        for i in self.puffers:
            if self.terminate:
                return
            log.debug('P1Seq.run() activate puffer id %d' % i)
            time.sleep(0.2)

    def event(self, event):
        if event in [EventQuit()]:
            self.terminate = True

class P2Seq(Mode):
    def __init__(self, config):
        Mode.__init__(self, config)
        self.puffers = config['small_puffers']['ids']

    def run(self):
        log.debug('P2Seq.run()')
        for i in reversed(self.puffers):
            if self.terminate:
                return
            log.debug('P2Seq.run() activate puffer id %d' % i)
            time.sleep(0.2)

    def event(self, event):
        if event in [EventQuit()]:
            self.terminate = True

if __name__ == '__main__':
    log.basicConfig(level=logging.DEBUG)
    m = CounterMode(start=1, end=5, time=0.3)
    m.thread.start()
    m.thread.join()


