import abc
import os

class Buttons(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getEmergencyStop(self):
        """ return True if emergency stop button is activated """
        pass

    @abc.abstractmethod
    def getStartButton(self):
        """ return True if Start button is pressed """
        pass

class SimButtons(Buttons):
    def getEmergencyStop(self):
        return os.path.exists('halt')

    def getStartButton(self):
        return os.path.exists('start')

if __name__ == '__main__':
    import time
    b = SimButtons();
    while True:
        print("stop=%s start=%s" % (b.getEmergencyStop(), b.getStartButton()))
        time.sleep(0.5)
    
