import abc
import logging
import time
import threading
log = logging

import fire_pong.util

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

class DebugEventsMode(Mode):
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
    from fire_pong.inputevents import *
    log.basicConfig(level=logging.DEBUG)
    m = DebugEventsMode()
    m.thread.start()
    for e in [InputMessageEvent('bananas'), InputSwipeEvent('1UP', 128)]:
        time.sleep(0.5)
        m.event(e)
    m.shutdown()
    m.thread.join()

