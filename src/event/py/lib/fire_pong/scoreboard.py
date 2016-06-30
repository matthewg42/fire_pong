from fire_pong.fp_event import FpEvent
import logging

log = logging

# Follows the singleton pattern
class ScoreBoard:
    class __ScoreBoard:
        def __init__(self, config, serial):
            self.config = config
            self.serial = serial

        def get_id(self):
            try:
                return self.config['display']['id']
            except:
                return None

        def display(self, message):
            disp_id = self.get_id()
            if disp_id is not None:
                e = FpEvent(disp_id, 'FP_EVENT_DISPLAY', message)
                log.debug('ScoreBoard SEND: %s' % str(e))
                self.serial.write(e.serialize())

    instance = None

    def __init__(self, config={}, serial={}):
        if not ScoreBoard.instance:
            ScoreBoard.instance = ScoreBoard.__ScoreBoard(config, serial)
        
    def __getattr__(self, name):
        return getattr(self.instance, name)

if __name__ == '__main__':
    import serial
    import os

    log.basicConfig(level=logging.DEBUG)

    config = {'display': {'id': 0x8000}}
    ser = None
    
    for port in ['/dev/ttyUSB0','/dev/ttyACM0']:
        if os.path.exists(port):
            ser = serial.Serial(port=port, baudrate=115200)

    sb = ScoreBoard(config, ser)
    
    # we can use the object
    sb.display('hi')

    # or, now it's initialized, we can also use the singleton approach...
    ScoreBoard().display('bananas')
    



