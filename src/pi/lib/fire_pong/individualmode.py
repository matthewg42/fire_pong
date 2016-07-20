import time
import threading
import struct
from fire_pong.util import log, config
from fire_pong.mode import Mode
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.modemanager import ModeManager

class IndividualMode(Mode):
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

