import serial

Bus = serial.Serial(port='/dev/ttyUSB0', 
                    baudrate=115200, 
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS)

def 
