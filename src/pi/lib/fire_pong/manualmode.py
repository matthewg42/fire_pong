import time
import threading
import random
from os import listdir
from struct import pack, unpack
from fire_pong.util import log, config
from fire_pong.mode import Mode
from fire_pong.events import *
from fire_pong.scoreboard import ScoreBoard
from fire_pong.modemanager import ModeManager
from fire_pong.fp_event import FpEvent
from fire_pong.fp_serial import FpSerial


class ManualMode(Mode):
    __displayname__ = 'Manual Mode'
    ''' Make puffs happen with buttons
        START button: random small puffer
        SWIPE1 large puff 1
        SWIPE2 large puff 2 '''
    def __init__(self):
        Mode.__init__(self)
        log.debug('ManualMode.__init__()')
        self.small_puffers = config['PongGame']['puffers']
        self.large_puffers = config['LargePuffers']['ids']
        self.puff_duration = config['ManualMode']['puff_duration']
        self.puff_type = 'FP_EVENT_ALTPUFF' if config['PongGame']['use_alt_puff'] else 'FP_EVENT_PUFF'
        self.puffer_mask =  0

    def run(self):
        log.debug('ManualMode.run() START')
        ScoreBoard().display('Yellow=random small puff; Green=Large 1; Blue=Large 2')
        while not self.terminate:
            if self.puffer_mask != 0:
                e = FpEvent(self.puffer_mask, self.puff_type, pack('<H', self.puff_duration))
                log.info('Event: %s' % str(e))
                FpSerial().write(e.serialize())
                self.puffer_mask = 0
            time.sleep(0.1)

        log.debug('ManualMode.run() END')

    def event(self, event):
        log.debug('ManualMode.event(%s)' % str(event))
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            self.puffer_mask = self.puffer_mask | self.small_puffers[random.randint(0, len(self.small_puffers)-1)]

        if type(event) is EventSwipe:
            if event.player == '2UP': 
                self.puffer_mask = self.puffer_mask | self.large_puffers[0]
            else:
                self.puffer_mask = self.puffer_mask | self.large_puffers[-1]

