import time
import threading
import struct
from fire_pong.util import log, config
from fire_pong.mode import Mode
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
from fire_pong.fp_event import FpEvent
from fire_pong.fp_serial import FpSerial
from fire_pong.menumode import MenuMode

class SetupMenuMode(MenuMode):
    __displayname__ = 'SU'
    def __init__(self):
        MenuMode.__init__(self, [TestSparkers, TestSolenoids])

class TestSparkers(Mode):
    __displayname__ = 'SP'
    RELAY_ON = struct.pack('<H', 0)
    RELAY_OFF = struct.pack('<H', 1)
    ''' Spark a single spearker, selected with swipes '''
    def __init__(self):
        log.debug('TestSparkers.__init__() START')
        Mode.__init__(self)
        self.puffers = config['PongGame']['puffers']
        self.duration = 1  # in seconds
        self.idx = 0
        self.display = True
        self.activate = False

    def run(self):
        log.debug('TestSparkers.run() START')
        while not self.terminate:
            if self.activate:
                self.activate = False
                self.start_spark()
                time.sleep(self.duration)
                self.stop_spark()
            if self.display:
                log.info('TestSparkers select puffer idx=%d; id=0x%08X; press START to activate' % (self.idx, self.puffers[self.idx]))
                ScoreBoard().display('%02d' % self.idx)
                self.display = False
            time.sleep(0.2)
        log.debug('TestSparkers.run() END')
        return None

    def start_spark(self):
        log.info("SPARK START idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
        e = FpEvent(self.puffers[self.idx], 'FP_EVENT_SPARK', self.RELAY_ON)
        log.info(str(e))
        FpSerial().write(e.serialize())

    def stop_spark(self):
        log.info("SPARK STOP idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
        e = FpEvent(self.puffers[self.idx], 'FP_EVENT_SPARK', self.RELAY_OFF)
        log.info(str(e))
        FpSerial().write(e.serialize())
        
    def event(self, event):
        log.debug('TestSparkers.event: received %s' % str(event))
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

class TestSolenoids(Mode):
    __displayname__ = 'SO'
    RELAY_ON = struct.pack('<H', 0)
    RELAY_OFF = struct.pack('<H', 1)
    ''' Spark a single spearker, selected with swipes '''
    def __init__(self):
        log.debug('TestSolenoids.__init__() START')
        Mode.__init__(self)
        self.puffers = config['PongGame']['puffers']
        self.puffers.extend(config['LargePuffers']['ids'])
        self.duration = 1  # in seconds
        self.idx = 0
        self.display = True
        self.activate = False

    def run(self):
        log.debug('TestSolenoids.run() START')
        while not self.terminate:
            if self.activate:
                self.activate = False
                self.start_solenoid()
                time.sleep(self.duration)
                self.stop_solenoid()
            if self.display:
                log.info('TestSolenoids select puffer idx=%d; id=0x%08X; press START to activate' % (self.idx, self.puffers[self.idx]))
                ScoreBoard().display('%02d' % self.idx)
                self.display = False
            time.sleep(0.2)
        log.debug('TestSolenoids.run() END')
        return None

    def start_solenoid(self):
        log.info("SOLENOID START idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
        e = FpEvent(self.puffers[self.idx], 'FP_EVENT_SOLENOID', self.RELAY_ON)
        log.info(str(e))
        FpSerial().write(e.serialize())

    def stop_solenoid(self):
        log.info("SOLENOID STOP idx=%02d id=%08X" % (self.idx, self.puffers[self.idx]))
        e = FpEvent(self.puffers[self.idx], 'FP_EVENT_SOLENOID', self.RELAY_OFF)
        log.info(str(e))
        FpSerial().write(e.serialize())
        
    def event(self, event):
        log.debug('TestSolenoids.event: received %s' % str(event))
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

