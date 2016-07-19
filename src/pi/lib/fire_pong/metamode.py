import time
import threading
import struct
import fire_pong.util
from random import randint
from fire_pong.mode import Mode
from fire_pong.fp_event import FpEvent
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.fp_serial import FpSerial
from fire_pong.modemanager import ModeManager
from fire_pong.pongmode import PongMode, PongVictory
from fire_pong.continuousmode import ContinuousMode
from fire_pong.singlemode import SingleMode
from fire_pong.util import log

# A mode for selecting other modes

class MetaMode(Mode):
    ''' Allows switching between modes '''
    def __init__(self):
        Mode.__init__(self)
        self.modes = [ PongMode, ContinuousMode, SingleMode, PongVictory, QuitMode ]
        self.idx = 0
        self.display = True
        self.activate = False

    def run(self):
        log.debug('MetaMode.run() START')
        while not self.terminate:
            if self.activate:
                self.activate = False
                if self.modes[self.idx] is QuitMode:
                    return 'Quit'
                else:
                    try:
                        ModeManager().push_mode(self.modes[self.idx]())
                    except Exception as e:
                        log.exception('in mode %s : %s : %s' % (self.modes[self.idx].__name__, type(e), e))
            if self.display:
                log.info('MetaMode selection: %s; press START to activate' % self.modes[self.idx].__name__)
                ScoreBoard().display(self.modes[self.idx].displayname())
                self.display = False
            time.sleep(0.2)
        log.debug('MetaMode.run() END')
        return 'END'
        
    def event(self, event):
        log.debug('MetaMode.event: received %s' % str(event))
        if event == EventQuit():
            self.idx = (self.idx + 1) % len(self.modes)
            self.display = True

        if event == EventButton('start'):
            log.info('MetaMode.event activating mode %s' % self.modes[self.idx].__name__)
            self.display = True
            # we can't actually push a mode in an event handler, so we set the flag to do it in the main loop instead
            self.activate = True

class QuitMode(Mode):
    def __init__(self):
        Mode.__init__(self)
        __displayname__ = 'Q'

    def run(self):
        return

    def event(self, event):
        return


