import abc
import time
import threading

import fire_pong.util
from fire_pong.util import log

class Mode(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self.terminate = False
        self.thread = threading.Thread(target=self.run)

    @abc.abstractmethod
    def run(self):
        return

    @abc.abstractmethod
    def event(self, event):
        return

    def shutdown(self):
        self.terminate = True

    @classmethod
    def displayname(cls):
        ''' returns a short (no more than 2 characters) name for use on the display in MenuMode '''
        try:
            # if class.__displayname__ is defined, use that
            return cls.__displayname__
        except Exception as e:
            log.debug('could not find __displayname__ class variable: %s: %s' % (type(e), e))
            # otherwise just use the first character of the mode class name
            # capitalized.
            return cls.__name__[0].upper()

class DebugEventsMode(Mode):
    __displayname__ = 'Debug Events'
    def __init__(self):
        Mode.__init__(self)

    def run(self):
        print("DebugEventsMode.run()")
        while not self.terminate:
            time.sleep(2)

    def event(self, event):
        log.debug('DebugEventsMode: %s' % event)

if __name__ == '__main__':
    import threading
    from fire_pong.events import *
    import logging
    log = logging
    log.basicConfig(level=logging.DEBUG)
    log.info('DebugEventsMode.displayname() = %s' % DebugEventsMode.displayname())
    m = DebugEventsMode()
    m.thread.start()
    for e in [EventMessage('bananas'), EventSwipe('1UP', 128)]:
        time.sleep(0.5)
        m.event(e)
    m.shutdown()
    m.thread.join()

