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

    
