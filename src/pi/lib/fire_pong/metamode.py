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
from fire_pong.fp_serial import FpSerial
from fire_pong.modemanager import ModeManager
from fire_pong.pongmode import *
from fire_pong.continuousmode import *
from fire_pong.singlemode import *

log = logging

# A mode for selecting other modes

class MetaMode(Mode):
    ''' Allows switching between modes '''
    def __init__(self):
        Mode.__init__(self)
        self.modes = [
            {'name': 'ContinuousModeManager',   'display': 'C', 'mode': ContinuousModeManager()},
            {'name': 'SingleMode',              'display': 'S', 'mode': SingleMode()},
            {'name': 'PongMatch',               'display': 'P', 'mode': PongMatch()}
        ]
        self.idx = 0
        self.display = True
        self.activate = False

    def run(self):
        log.debug('MetaMode.run() START')
        while not self.terminate:
            if self.activate:
                self.activate = False
                ModeManager().push_mode(self.modes[self.idx]['mode'])
            if self.display:
                print('MetaMode selection: %s; press START to activate' % self.modes[self.idx]['name'])
                ScoreBoard().display(self.modes[self.idx]['display'])
                self.display = False
            time.sleep(0.2)
        log.debug('MetaMode.run() END')
        
    # if ModeManager().push_mode(ContinuousModePuffs()) is None:

    def event(self, event):
        log.debug('MetaMode.event: received %s' % str(event))
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            log.info('MetaMode.event activating mode %s' % self.modes[self.idx]['name'])
            self.display = True
            # we can't actually push a mode in an event handler, so we set the flag to do it in the main loop instead
            self.activate = True

        if type(event) is EventSwipe:
            if event.player == '2UP': 
                self.idx = (self.idx + 1) % len(self.modes)
            else:
                self.idx = (self.idx - 1) % len(self.modes)
            self.display = True
