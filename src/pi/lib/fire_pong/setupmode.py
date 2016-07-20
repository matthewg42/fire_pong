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
from fire_pong.individualmode import IndividualMode

class SetupMenuMode(MenuMode):
    __displayname__ = 'SU'
    def __init__(self):
        MenuMode.__init__(self, [TestSparker, TestSolenoid, SinglePuff, LargePuff, LargePuffCycle])

class TestSparker(IndividualMode):
    __displayname__ = 'SP'
    RELAY_ON = struct.pack('<B', 0)
    RELAY_OFF = struct.pack('<B', 1)
    ''' Spark a single spearker, selected with swipes '''
    def __init__(self):
        puffers = config['PongGame']['puffers']
        IndividualMode.__init__(self, puffers, self.callback)
        self.duration = 0.5  # in seconds

    def callback(self, idmask):
        log.info("SPARK START id=%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_SPARK', self.RELAY_ON)
        log.info(str(e))
        FpSerial().write(e.serialize())
        time.sleep(self.duration)
        log.info("SPARK STOP id%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_SPARK', self.RELAY_OFF)
        log.info(str(e))
        FpSerial().write(e.serialize())
        
class TestSolenoid(IndividualMode):
    ''' Open and then close a single solenoid, selected with swipes '''
    __displayname__ = 'SO'
    RELAY_ON = struct.pack('<B', 0)
    RELAY_OFF = struct.pack('<B', 1)
    def __init__(self):
        puffers = config['PongGame']['puffers']
        IndividualMode.__init__(self, puffers, self.callback)
        self.duration = 1.5  # in seconds

    def callback(self, idmask):
        log.info("SOLENOID OPEN id=%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_SOLENOID', self.RELAY_ON)
        log.info(str(e))
        FpSerial().write(e.serialize())
        time.sleep(self.duration)
        log.info("SOLENOID CLOSE id%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_SOLENOID', self.RELAY_OFF)
        log.info(str(e))
        FpSerial().write(e.serialize())
    
class SinglePuff(IndividualMode):
    ''' Call puff sequence for a single puffer '''
    __displayname__ = 'IP'
    def __init__(self):
        puffers = config['PongGame']['puffers']
        IndividualMode.__init__(self, puffers, self.callback)
        self.duration = config['PongGame']['puff_duration']

    def callback(self, idmask):
        log.info("PUFF id=%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_PUFF', struct.pack('<H', self.duration))
        log.info(str(e))
        FpSerial().write(e.serialize())

class LargePuff(IndividualMode):
    ''' Do a long puff for a big puffer '''
    __displayname__ = 'LP'
    def __init__(self):
        puffers = config['LargePuffers']['ids']
        IndividualMode.__init__(self, puffers, self.callback)
        self.duration = config['LargePuffers']['puff_duration']

    def callback(self, idmask):
        log.info("PUFF id=%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_PUFF', struct.pack('<H', self.duration))
        log.info(str(e))
        FpSerial().write(e.serialize())

class LargePuffCycle(IndividualMode):
    ''' Do a very long puff for a bif puffer (used while cycling accumulator '''
    __displayname__ = 'LC'
    def __init__(self):
        puffers = config['LargePuffers']['ids']
        IndividualMode.__init__(self, puffers, self.callback)
        self.duration = config['LargePuffers']['cycle_duration']

    def callback(self, idmask):
        log.info("PUFF id=%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_PUFF', struct.pack('<H', self.duration))
        log.info(str(e))
        FpSerial().write(e.serialize())
        
    
