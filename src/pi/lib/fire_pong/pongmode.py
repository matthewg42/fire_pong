import time
import threading
import struct
import fire_pong.util
from random import randint
from fire_pong.util import log
from fire_pong.mode import Mode
from fire_pong.fp_event import FpEvent
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
from fire_pong.fp_serial import FpSerial

def strength2delay(strength):
    d = 0.8 - (float(strength)/300)
    if d <= 0.2:
        d = 0.2
    return d

class PongMode(Mode):
    def __init__(self):
        Mode.__init__(self)
        self.winning_score = fire_pong.util.config['PongMatch']['winning_score']
        self.start_player = randint(1, 2)

    def reset(self):
        log.info('PongMode: NEW MATCH')
        self.score = [0,0]

    def display_score(self):
        ScoreBoard().display('%d%d' % tuple(self.score))

    def run(self):
        log.debug('PongMode.run() START')

        while not self.terminate:
            self.reset()
            while max(self.score) < self.winning_score and not self.terminate:
                self.display_score()
                if ModeManager().push_mode(PongWaitStart()) is False:
                    return 'PongMode Quit'
                if ModeManager().push_mode(PongCounterMode(start=3, end=1)) is False:
                    return 'PongMode Quit'
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
                ModeManager().push_mode(PongVictory(win))
            elif self.score[1] > self.score[0]:
                log.info("Player 2 wins")
                ScoreBoard().display("2W")
                ModeManager().push_mode(PongVictory(win))
            else:
                log.info("It's a DRAW!")
                ScoreBoard().display("Dr")

        log.debug('PongMode.run() END')

    def event(self, event):
        if event == EventQuit():
            self.terminate = True

class PongWaitStart(Mode):
    def __init__(self):
        Mode.__init__(self)
        self.start = True

    def run(self):
        ''' return False if Quit event received, True is Start event received '''
        log.debug('PongWaitStart.run() START')
        while not self.terminate:
            time.sleep(0.5)
        log.debug('PongWaitStart.run() END')
        return self.start
        
    def event(self, event):
        if event == EventButton('start'):
            self.start = True
            self.terminate = True
        if event == EventQuit():
            self.start = False
            self.terminate = True

class PongCounterMode(Mode):
    ''' Countdown for beginning games 
        returns False if Quit pressed, else True '''
    
    def __init__(self, start=3, end=1, time=1):
        Mode.__init__(self)
        self.start = True
        self.count = start
        self.end = end
        if start > end:
            self.step = -1
        else:
            self.step = +1
        self.time = time

    def run(self):
        log.debug('PongCounterMode.run()')
        while not self.terminate and self.count != self.end + self.step:
            ScoreBoard().display(str(self.count))
            self.count += self.step
            time.sleep(self.time)
        log.debug('PongCounterMode.run() END %s' % self.start)
        return self.start

    def event(self, event):
        if event == EventButton('start'):
            self.start = True
            self.terminate = True
        if event == EventQuit():
            self.start = False
            self.terminate = True

class PongGame(Mode):
    def __init__(self, start_player):
        Mode.__init__(self)
        self.puffers = fire_pong.util.config['PongGame']['puffers']
        self.delay = fire_pong.util.config['PongGame']['initial_delay']
        self.puff_duration = fire_pong.util.config['PongGame']['puff_duration']
        self.hit_idx = {'1UP': [0, 1], '2UP': [len(self.puffers)-2, len(self.puffers)-1]}
        self.win = None
        self.quit = False
        self.start_player = start_player
        if self.start_player == 1:
            self.idx = 0
            self.inc = 1
        else:
            self.idx = len(self.puffers)-1
            self.inc = -1

    def run(self):
        ''' Return None if Quit was pressed, else return the winner of the game, i.e. 1 or 2 '''
        log.debug('PongGame.run()')
            
        while self.win is None:
            if self.terminate:
                return
            if self.idx < 0:
                self.win = 2
                break
            elif self.idx >= len(self.puffers):
                self.win = 1
                break
            elif self.idx >= 0 and self.idx < len(self.puffers):
                d = ['', '', '']
                for i in range(0, len(self.puffers)):
                    d[0] += '   ' if i != self.idx else ' @ '
                    d[1] += '   ' if i != self.idx else ' @ '
                    d[2] += ' | ' if i != self.idx else ' | '
                for i in range(0,3):
                    log.info(d[i])
                log.info("PUFF idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
                e = FpEvent(self.puffers[self.idx], 'FP_EVENT_PUFF', struct.pack('<H', self.puff_duration))
                log.info(str(e))
                FpSerial().write(e.serialize())
            time.sleep(self.delay)
            self.idx += self.inc
        if self.quit:
            return None
        else:
            return self.win
            
    def event(self, event):
        if event == EventQuit():
            self.quit = True
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

class PongVictory(Mode):
    ''' Wait for player to swipe, and then do single fast run of small
        puffers, followed by single big puffer next to ossposing player '''
    def __init__(self, player=None):
        Mode.__init__(self)
        if player == None:
            player = randint(1, 2)
        self.player = player
        self.puffers = fire_pong.util.config['PongGame']['puffers']
        self.puff_duration = fire_pong.util.config['PongGame']['puff_duration']
        self.large_puff_duration_ms = 100
        self.idx = 0
        if player == 1:
            self.large_puffer = fire_pong.util.config['LargePuffers']['ids'][0]
        else:
            self.puffers.reverse()
            self.large_puffer = fire_pong.util.config['LargePuffers']['ids'][1]
        self.delay = None

    def run(self):
        log.debug('PongVictory.run() START')
        # Wait for a swipe (indicated by setting self.delay to not None)
        ScoreBoard().display('V%d' % self.player)
        log.info('Waiting for player %d swipe...' % self.player)
        while self.terminate is False and self.delay is None:
            time.sleep(0.1)
        if self.terminate:
            return False

        while self.idx < len(self.puffers):
            if self.terminate:
                return 'Quit'
            self.pic(False)
            log.info("PUFF idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
            e = FpEvent(self.puffers[self.idx], 'FP_EVENT_PUFF', struct.pack('<H', self.puff_duration))
            log.info(str(e))
            FpSerial().write(e.serialize())
            time.sleep(self.delay)
            self.idx += 1
        self.pic(True)
        log.info('LARGE PUFFER id=%08X duration (ms)=%d' % (self.large_puffer, self.large_puff_duration_ms))
        e = FpEvent(self.large_puffer, 'FP_EVENT_PUFF', struct.pack('<H', self.large_puff_duration_ms))
        FpSerial().write(e.serialize())
            
    def pic(self, large=False):
        d = ['', '', '']
        for i in range(0, len(self.puffers)):
            d[0] += '   ' if i != self.idx else ' @ '
            d[1] += '   ' if i != self.idx else ' @ '
            d[2] += ' | ' if i != self.idx else ' | '
        d[0] += ' @ ' if large else '   '
        d[1] += ' | '
        d[2] += ' 0 '
        for i in range(0,3):
                log.info(d[i])

    def event(self, event):
        log.info('PongVictory.debug: %s' % event)
        strength = None
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            strength = randint(20,120)
        if type(event) is EventSwipe:
            if event.player == '%dUP' % self.player:
                strength = event.strength

            if strength:
                self.delay = strength2delay(strength) / 3.0
                self.large_puff_duration_ms = 100.0 / self.delay
                log.info("Player %s VICTORY SWIPE (str=%s) => delay=%s; bigg puff=%s" % (
                            event.player, 
                            event.strength, 
                            self.delay,
                            self.large_puff_duration_ms))

if __name__ == '__main__':
    import logging
    log = logging
    log.basicConfig(level=logging.DEBUG)
    m = PongCounterMode(start=1, end=5, time=0.3)
    m.thread.start()
    m.thread.join()


