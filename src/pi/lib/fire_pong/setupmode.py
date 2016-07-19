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
        MenuMode.__init__(self, [TestSparker, TestSolenoid, SinglePuff])

class IndiviualMode(Mode):
    ''' A mode which allows some operation to be called for individual IDs
        This in intended to be sub-classed for SinglePuff, Sparktest, 
        SolenoidTest and so on.

        callback is called for a selected id, with the id as the argument '''
    def __init__(self, ids, callback):
        Mode.__init__(self)
        log.debug('%s.__init__(ids=%s, callback=%s) START' % (
                        str(ids), 
                        str(callback), 
                        self.__class__.__name__))
        self.ids = ids
        self.callback = callback
        self.idx = 0
        self.display = True
        self.activate = False
        
    def run(self):
        log.debug('%s.run() START' % self.__class__.__name__)
        while not self.terminate:
            if self.activate:
                self.activate = False
                self.callback(self.ids[self.idx])
            if self.display:
                log.info('%s.run() select puffer idx=%d; id=0x%08X; press START to activate' % (
                    self.__class__.__name__, self.idx, self.ids[self.idx]))
                ScoreBoard().display('%02d' % self.idx)
                self.display = False
            time.sleep(0.2)
        log.debug('%s.run() END' % self.__class__.__name__)
        return None

    def event(self, event):
        log.debug('%s.event(%s)' % (self.__class__.__name__, str(event)))
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            self.activate = True

        if type(event) is EventSwipe:
            if event.player == '2UP': 
                self.idx = (self.idx + 1) % len(self.ids)
            else:
                self.idx = (self.idx - 1) % len(self.ids)
            self.display = True

class TestSparker(IndiviualMode):
    __displayname__ = 'SP'
    RELAY_ON = struct.pack('<H', 0)
    RELAY_OFF = struct.pack('<H', 1)
    ''' Spark a single spearker, selected with swipes '''
    def __init__(self):
        puffers = config['PongGame']['puffers']
        IndiviualMode.__init__(self, puffers, self.callback)
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
        
class TestSolenoid(IndiviualMode):
    ''' Open and then close a single solenoid, selected with swipes '''
    __displayname__ = 'SO'
    RELAY_ON = struct.pack('<H', 0)
    RELAY_OFF = struct.pack('<H', 1)
    def __init__(self):
        puffers = config['PongGame']['puffers']
        IndiviualMode.__init__(self, puffers, self.callback)
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
    
class SinglePuff(IndiviualMode):
    ''' Call puff sequence for a single puffer '''
    __displayname__ = 'IP'
    def __init__(self):
        puffers = config['PongGame']['puffers']
        IndiviualMode.__init__(self, puffers, self.callback)
        self.duration = config['PongGame']['puff_duration']

    def callback(self, idmask):
        log.info("PUFF id=%08X" % idmask)
        e = FpEvent(idmask, 'FP_EVENT_PUFF', struct.pack('<H', self.duration))
        log.info(str(e))
        FpSerial().write(e.serialize())

        
    
