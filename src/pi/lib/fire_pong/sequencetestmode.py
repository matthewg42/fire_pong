import time
import threading
import random
from os import listdir
from struct import pack, unpack
from fire_pong.util import log, config
from fire_pong.mode import Mode
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
from fire_pong.scoreboard import ScoreBoard
from fire_pong.fp_event import FpEvent
from fire_pong.fp_serial import FpSerial
from fire_pong.menumode import MenuMode

class SequenceTestMode(MenuMode):
    __displayname__ = 'ST'
    def __init__(self):
        MenuMode.__init__(self, [Sequence1, Sequence2, Sequence3])

class SmallPufferSequence(Mode):
    ''' to be sub-classed - will execute sequence member function on a
        random small puffer whenever the start button is pressed '''
    RELAY_ON = pack('<B', 0)
    RELAY_OFF = pack('<B', 1)
    def __init__(self):
        Mode.__init__(self)
        self.puffers = config['PongGame']['puffers']
        self.idx = None

    def run(self):
        log.debug('%s.run() START' % self.__class__.__name__)
        ScoreBoard().display(self.__displayname__.lower())
        try:
            while not self.terminate:
                if self.idx:
                    log.debug('%s.run() calling sequence' % self.__class__.__name__)
                    self.sequence(self.puffers[self.idx])
                    self.idx = None
                time.sleep(0.1)
            log.debug('%s.run() END' % self.__class__.__name__)
        finally:
            # When leaving mode make sure all relays are OFF!
            for i in range(0, len(self.puffers)):
                self.spark(self.puffers[i], on=False)
                self.solenoid(self.puffers[i], on=False)

    def event(self, event):
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            self.idx = random.randint(0,len(self.puffers)-1)

    def spark(self, pufferid, on=False):
        e = FpEvent(pufferid, 'FP_EVENT_SPARK', SmallPufferSequence.RELAY_ON if on else SmallPufferSequence.RELAY_OFF)
        log.info('%s.spark() sending: %s' % (self.__class__.__name__, str(e)))
        FpSerial().write(e.serialize())

    def solenoid(self, pufferid, on=False):
        e = FpEvent(pufferid, 'FP_EVENT_SOLENOID', SmallPufferSequence.RELAY_ON if on else SmallPufferSequence.RELAY_OFF)
        log.info('%s.solenoid() sending: %s' % (self.__class__.__name__, str(e)))
        FpSerial().write(e.serialize())

class Sequence1(SmallPufferSequence):
    __displayname__ = 'S1'
    def sequence(self, pufferid):
        log.info('Current Firmware Sequence with 150ms main puff length...')
        self.spark(pufferid, on=True)
        time.sleep(0.100)
        self.solenoid(pufferid, on=True)
        time.sleep(0.013)
        self.solenoid(pufferid, on=False)
        time.sleep(0.200)
        self.solenoid(pufferid, on=True)
        time.sleep(0.150)
        self.solenoid(pufferid, on=False)
        time.sleep(0.100)
        self.spark(pufferid, on=False)

class Sequence2(SmallPufferSequence):
    __displayname__ = 'S2'
    def sequence(self, pufferid):
        log.info('Simple on off, with spark 200ms extra at start and end...')
        self.spark(pufferid, on=True)
        time.sleep(0.200)
        self.solenoid(pufferid, on=True)
        time.sleep(0.100)
        self.solenoid(pufferid, on=False)
        time.sleep(0.200)
        self.spark(pufferid, on=False)

class Sequence3(SmallPufferSequence):
    __displayname__ = 'S3'
    def sequence(self, pufferid):
        log.info('Simple on off, with spark 100ms extra at start and end...')
        self.spark(pufferid, on=True)
        time.sleep(0.100)
        self.solenoid(pufferid, on=True)
        time.sleep(0.100)
        self.solenoid(pufferid, on=False)
        time.sleep(0.100)
        self.spark(pufferid, on=False)


