
import logging
import serial

log = logging

def open_serial(config):
    c = config['serial']
    defaults = {'baudrate': 115200, 'parity': 'none', 'stopbits': 2, 'bytesize': 8}
    for k, v in defaults.items():
        if k not in c:
            c[k] = v
    # translate text to serial param names
    c['parity'] = {'none': serial.PARITY_NONE, 'odd': serial.PARITY_ODD, 'even': serial.PARITY_EVEN}[c['parity']]
    c['stopbits'] = {1: serial.STOPBITS_ONE, 2: serial.STOPBITS_TWO}[c['stopbits']]
    c['bytesize'] = {8: serial.EIGHTBITS, 7: serial.SEVENBITS}[c['bytesize']]
    ser = serial.Serial(port=c['port'], parity=c['parity'], stopbits=c['stopbits'], bytesize=c['bytesize'])
    ser.isOpen()
    return ser

