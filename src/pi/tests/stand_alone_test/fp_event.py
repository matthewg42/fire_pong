""" FpEvents are serializable events for Fire Pong
"""

from crc8 import crc8
import struct
import logging

log = logging

class FpEvent():
    def __init__(self, id_set, fp_type, data=b''):
        self.id_set = id_set
        if fp_type in FpEvent.FP_TYPES.values():
            self.fp_type = FpEvent.get_type_id(fp_type)
        elif fp_type not in FpEvent.FP_TYPES.keys():
            raise Exception("unknown event type: %s" % fp_type)
        else:
            self.fp_type = fp_type
        if len(data) > FpEvent.FP_MAX_DATA_LEN:
            raise Exception('data length too large (len=%s, max=%s)' % (len(data), FpEvent.FP_MAX_DATA_LEN))
        self.data = data
        self.checksum = 0xCC
        self.checksum = self.calculate_checksum()

    def __str__(self):
        return 'FpEvent: id_set=0x%04x, type=%d/%s, data=%s, cksum=%s [%s:0x%02x] valid=%s' % (
                self.id_set,
                self.fp_type,
                FpEvent.FP_TYPES[self.fp_type],
                self.data,
                '--' if self.checksum is None else '0x%02x' % self.checksum,
                'GOOD' if self.calculate_checksum() == self.checksum else 'BAD',
                self.calculate_checksum(),
                self.is_valid()
            )

    def serialize(self):
        pack = FpEvent.FP_PACK%len(self.data)
        return struct.pack(pack, FpEvent.FP_MAGIC, struct.calcsize(pack), 
                                 self.id_set, self.fp_type, self.data, 
                                 self.checksum, FpEvent.FP_MAGIC)

    def calculate_checksum(self):
        data = self.serialize()
        length = struct.unpack('<B', data[2])[0]
        return crc8(data, length-3)

    def validate_checksum(self):
        return self.checksum == self.calculate_checksum()

    def is_valid(self):
        return self.validate_checksum()

    @classmethod
    def from_bytes(cls, b): 
        """ Make a new FpEvent from a serialized blob of bytes """
        (magic, length) = struct.unpack('<HB', b[0:struct.calcsize('<HB')])
        if magic != FpEvent.FP_MAGIC:
            raise Exception('Serial packet did not start with magic')
        length = int(length)
        if length > FpEvent.FP_MAX_PACKET_LEN:
            raise Exception('Packet length too long')
        data_length = length - struct.calcsize(FpEvent.FP_PACK%0)
        unp = FpEvent.FP_PACK % data_length
        (magic, length, id_set, fp_type, data, checksum, magic2) = struct.unpack(unp, b)
        e = cls(id_set, fp_type, data)
        e.checksum = checksum
        return e

    FP_MAX_DATA_LEN = 16
    FP_MAGIC = 0x5066
    FP_PACK = '<HBIB%dsBH'
    FP_MAX_PACKET_LEN = struct.calcsize(FP_PACK%FP_MAX_DATA_LEN)
    FP_TYPES = { 0: 'FP_EVENT_HALT', 
                 1: 'FP_EVENT_RESET', 
                 2: 'FP_EVENT_SPARK', 
                 3: 'FP_EVENT_SOLENOID', 
                 4: 'FP_EVENT_PUFF', 
                 5: 'FP_EVENT_DISPLAY',
                 6: 'FP_EVENT_RELAY' } 
    @classmethod
    def get_type_id(cls, t):
        for key, value in cls.FP_TYPES.items():
            if value == t:
                return key
        return None
        
