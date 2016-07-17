
import serial as pyserial
import fire_pong.util 
from fire_pong.util import log

# Follows the singleton pattern
class FpSerial:
    class __FpSerial:
        def __init__(self):
            defaults = {'baudrate': 115200, 'parity': 'none', 'stopbits': 2, 'bytesize': 8}
            c = fire_pong.util.config['serial']
            for k, v in defaults.items():
                if k not in c:
                    c[k] = v
            # translate text to serial param names
            c['parity'] = {'none': pyserial.PARITY_NONE, 'odd': pyserial.PARITY_ODD, 'even': pyserial.PARITY_EVEN}[c['parity']]
            c['stopbits'] = {1: pyserial.STOPBITS_ONE, 2: pyserial.STOPBITS_TWO}[c['stopbits']]
            c['bytesize'] = {8: pyserial.EIGHTBITS, 7: pyserial.SEVENBITS}[c['bytesize']]
            log.debug('FpSerial serial config: %s' % c)
            self.serial = pyserial.Serial(port=c['port'], baudrate=c['baudrate'], parity=c['parity'], stopbits=c['stopbits'], bytesize=c['bytesize'])
            self.serial.isOpen()

        def write(self, buf):
            if self.serial:
                if fire_pong.util.config['serial']['debug']:
                    log.debug('SERIAL WRITE: %3d bytes: %s [%s]' % (len(buf), repr(bytearray(buf)), ' '.join(['%02x' % ord(x) for x in buf])))
                self.serial.write(buf)
            else:
                log.warning('FpSerial.write() serial device not configured')

    instance = None

    def __init__(self):
        if not FpSerial.instance:
            FpSerial.instance = FpSerial.__FpSerial()
        
    def __getattr__(self, name):
        return getattr(self.instance, name)

