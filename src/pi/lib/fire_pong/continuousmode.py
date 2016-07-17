import time
import threading
import struct
import fire_pong.util
from fire_pong.util import log
from random import randint
from fire_pong.mode import Mode
from fire_pong.fp_event import FpEvent
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
from fire_pong.fp_serial import FpSerial

class ContinuousModeManager(Mode):
    ''' Cycle between waiting and continuous mode '''
    def __init__(self):
        Mode.__init__(self)

    def run(self):
        log.debug('ContinuousModeManager.run() START')
        while not self.terminate:
            if ModeManager().push_mode(ContinuousModeWait()) is None:
                return
            if ModeManager().push_mode(ContinuousModePuffs()) is None:
                return
        log.debug('ContinuousModeManager.run() END')
        
    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class ContinuousModeWait(Mode):
    def __init__(self):
        Mode.__init__(self)

    def run(self):
        log.debug('ContinuousModeWait.run() START')
        print("Continuous Mode. WAITING. Press START button to continue")
        while not self.terminate:
            time.sleep(0.5)
        log.debug('ContinuousModeWait.run() END')
        
    def event(self, event):
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

class ContinuousModePuffs(Mode):
    def __init__(self):
        Mode.__init__(self)
        self.puffers = fire_pong.util.config['PongGame']['puffers']
        self.delay = fire_pong.util.config['PongGame']['initial_delay']
        self.puff_duration = fire_pong.util.config['PongGame']['puff_duration']
        self.idx = 0
        self.inc = 1
        self.terminate = False

    def run(self):
        log.debug('ContinuousModePuffs.run() START')
            
        while self.terminate is False:
            # Print a little graphic of the puffers showing which one is active...
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

            # Move the frixel by inc
            self.idx += self.inc

            # Bounce if necessary
            if self.idx == -1:
                self.idx = 1
                self.inc = 1
            elif self.idx == len(self.puffers):
                self.idx = len(self.puffers) - 2
                self.inc = -1

            # Wait a little bit...
            time.sleep(self.delay)

        log.debug('ContinuousModePuffs.run() END')
            
    def event(self, event):
        log.debug('ContinuousModePuffs.event received: %s' % str(event))
        if event in [EventButton('start'), EventQuit()]:
            self.terminate = True

        if type(event) is EventSwipe:
            if event.player == '1UP':
                self.delay += 0.025
            else:
                self.delay -= 0.025
                if self.delay < 0.08:
                    self.delay = 0.08
            print('DELAY set to %s' % self.delay)

