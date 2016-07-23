import time
import threading
import struct
from fire_pong.util import log, config
from fire_pong.mode import Mode
from fire_pong.fp_event import FpEvent
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
from fire_pong.fp_serial import FpSerial
from fire_pong.scoreboard import ScoreBoard
from fire_pong.visualizer import Visualizer

class ContinuousMode(Mode):
    ''' Cycle between waiting and continuous mode '''
    __displayname__ = 'Continuous Puffs'
    def __init__(self):
        Mode.__init__(self)

    def run(self):
        log.debug('ContinuousMode.run() START')
        self.terminate = False
        while not self.terminate:
            if ModeManager().push_mode(ContinuousModeWait()) is False:
                self.terminate = True
                break
            else:
                ModeManager().push_mode(ContinuousModePuffs())
        log.debug('ContinuousMode.run() END')
        
    def event(self, event):
        if event == EventQuit():
            self.terminate = True

class ContinuousModeWait(Mode):
    def __init__(self):
        Mode.__init__(self)
        self.quit = False

    def run(self):
        log.debug('ContinuousModeWait.run() START')
        log.info("Continuous Mode. WAITING. Press START button to continue")
        ScoreBoard().display('CW')
        while not self.terminate:
            time.sleep(0.5)
        log.debug('ContinuousModeWait.run() END')
        if self.quit:
            return False
        else:
            return True
        
    def event(self, event):
        if event == EventQuit():
            self.terminate = True
            self.quit = True

        if event == EventButton('start'):
            self.terminate = True

class ContinuousModePuffs(Mode):
    def __init__(self):
        Mode.__init__(self)
        self.puffers = config['PongGame']['puffers']
        self.delay = config['PongGame']['initial_delay']
        self.puff_duration = config['PongGame']['puff_duration']
        self.puff_type = 'FP_EVENT_ALTPUFF' if config['PongGame']['use_alt_puff'] else 'FP_EVENT_PUFF'
        self.idx = 0
        self.inc = 1
        self.terminate = False

    def run(self):
        log.debug('ContinuousModePuffs.run() START')
            
        ScoreBoard().display('CP')
        while self.terminate is False:
            # Print a little graphic of the puffers showing which one is active...
            log.info("%s idx=%02d id=%08X" % (self.puff_type, self.idx, self.puffers[self.idx]))
            e = FpEvent(self.puffers[self.idx], self.puff_type, struct.pack('<H', self.puff_duration))
            log.info(str(e))
            Visualizer().info(e)
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
            log.info('DELAY set to %s' % self.delay)

