import time
import threading
import struct
from fire_pong.util import log
from fire_pong.mode import Mode
from fire_pong.scoreboard import ScoreBoard
from fire_pong.modemanager import ModeManager
from fire_pong.events import *

# A mode for selecting other modes

class MenuMode(Mode):
    ''' Allows selection of one of several other modes '''
    def __init__(self, modes):
        Mode.__init__(self)
        self.modes = modes 
        self.modes.append(QuitMode)
        self.idx = 0
        self.display = True
        self.activate = False

    def run(self):
        log.debug('%s.run() START' % self.__class__.__name__)
        while not self.terminate:
            if self.activate:
                self.activate = False
                if self.modes[self.idx] is QuitMode:
                    log.debug('%s.run() QuitMode selected' % self.__class__.__name__)
                    return 'Quit'
                else:
                    try:
                        ModeManager().push_mode(self.modes[self.idx]())
                    except Exception as e:
                        log.exception('in mode %s : %s : %s' % (self.modes[self.idx].__name__, type(e), e))
            if self.display:
                log.info('%s selection: %s; press START to activate' % (self.__class__.__name__, self.modes[self.idx].__name__))
                ScoreBoard().display(self.modes[self.idx].displayname())
                self.display = False
            time.sleep(0.2)
        log.debug('%s.run() END' % self.__class__.__name__)
        return 'END'
        
    def event(self, event):
        log.debug('%s.event(%s) START' % (self.__class__.__name__, str(event)))
        if event == EventQuit():
            self.idx = (self.idx + 1) % len(self.modes)
            self.display = True

        if event == EventButton('start'):
            log.info('%s.event() activating mode %s' % (self.__class__.__name__, self.modes[self.idx].__name__))
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


