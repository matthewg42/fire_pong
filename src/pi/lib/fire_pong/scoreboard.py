from fire_pong.fp_event import FpEvent
from fire_pong.fp_serial import FpSerial
from fire_pong.util import log
from fire_pong.keyboard import Keyboard
from fire_pong.visualizer import Visualizer
import fire_pong.util

# Follows the singleton pattern
class ScoreBoard:
    class __ScoreBoard:
        def __init__(self):
            log.debug('ScoreBoard display id=%08X' % self.get_id())
            self.keyboard = None
            self.muted = False
            try:
                self.keyboard = Keyboard()
            except Exception as e:
                log.info('Could not get Keyboard object (for screen display)')

        def get_id(self):
            return fire_pong.util.config['display']['id']

        def mute(self):
            self.muted = True

        def unmute(self):
            self.muted = False

        def display(self, message):
            message = str(message)[0:FpEvent.FP_MAX_DATA_LEN]
            disp_id = self.get_id()
            if disp_id is not None:
                e = FpEvent(disp_id, 'FP_EVENT_DISPLAY', message)
                log.info('DISPLAY: %s' % message)
                Visualizer().update(e)
                if self.muted is False:
                    FpSerial().write(e.serialize())
            if self.keyboard is not None:
                self.keyboard.display_text(message)

    instance = None

    def __init__(self):
        if not ScoreBoard.instance:
            ScoreBoard.instance = ScoreBoard.__ScoreBoard()
        
    def __getattr__(self, name):
        return getattr(self.instance, name)

if __name__ == '__main__':
    import logging
    log = logging
    log.basicConfig(level=logging.DEBUG)
    fire_pong.fp_serial.log = log
    fire_pong.util.config = {'display': { 'id': 0x1000 }, 
              'serial': {
                    'port': '/dev/ttyUSB0', 
                    'baudrate': 115200, 
                    'parity': 'none', 
                    'stopbits': 2, 
                    'bytesize': 8, 
                    'debug': True}}
    
    sb = ScoreBoard()
    
    # we can use the object
    sb.display('bananas')

    # or, now it's initialized, we can also use the singleton approach...
    ScoreBoard().display('hi')


