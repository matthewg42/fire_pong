from fire_pong.fp_event import FpEvent
import logging

log = logging

class ScoreBoard:
    def __init__(self, config, serial):
        self.display('BOOT')
        self.config = config
        self.serial = serial
        self.display('boot')

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


