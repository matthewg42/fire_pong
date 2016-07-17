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
from fire_pong.util import log

# A mode for selecting other modes

class SingleMode(Mode):
    ''' Allows switching between modes '''
    def __init__(self):
        Mode.__init__(self)
        self.puffers = fire_pong.util.config['PongGame']['puffers']
        self.puffers.extend(fire_pong.util.config['LargePuffers']['ids'])
        self.puff_duration = fire_pong.util.config['PongGame']['puff_duration']
        self.idx = 0
        self.display = True
        self.activate = False

    def run(self):
        log.debug('SingleMode.run() START')
        while not self.terminate:
            if self.activate:
                self.activate = False
                log.info("PUFF idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
                print('SingleMode PUFF')
                e = FpEvent(self.puffers[self.idx], 'FP_EVENT_PUFF', struct.pack('<H', self.puff_duration))
                print(str(e))
                FpSerial().write(e.serialize())
            if self.display:
                print('SingleMode select puffer idx=%d; id=0x%08X; press START to activate' % (self.idx, self.puffers[self.idx]))
                ScoreBoard().display('%02d' % self.idx)
                self.display = False
            time.sleep(0.2)
        log.debug('SingleMode.run() END')
        
    def event(self, event):
        log.debug('SingleMode.event: received %s' % str(event))
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            # set the flag to do the actual work in run()
            self.activate = True

        if type(event) is EventSwipe:
            if event.player == '2UP': 
                self.idx = (self.idx + 1) % len(self.puffers)
            else:
                self.idx = (self.idx - 1) % len(self.puffers)
            self.display = True

