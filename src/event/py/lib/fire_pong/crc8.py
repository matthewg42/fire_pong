
CRC8INIT = 0x00
CRC8POLY = 0x18

def crc8(data, length=None):
    if length is None:
        length = len(data)
    if length > len(data):
        raise Exception('length is bigger than the size of the provided data')
    crc = CRC8INIT   
    loop_count = 0
    for loop_count in range(0,length):
        b = data[loop_count]
        bit_counter = 8
        while True:
            feedback_bit = (crc ^ b) & 0x01;
            if feedback_bit == 0x01:
                crc = crc ^ CRC8POLY
            crc = int(crc/2) & 0x7F
            if feedback_bit == 0x01:
                crc = crc | 0x80
            b = int(b/2)
            bit_counter -= 1
            if bit_counter <= 0:
                break
    return crc


