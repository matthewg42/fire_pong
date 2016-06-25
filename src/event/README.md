# Fire Pong Event Processing Firmware

Monitors inputs and sends puff events to puffers on serial bus.

## Event Packets

All values are little endian. On an Arduino (which is already little endian), we don't need to 
swap any bytes around. If the master is not little-endian, it is the responsibility of the master on the bus to convert packets to little endian.

    |   | |       | |       | |   |
    |m|m|l|i|i|i|i|t|d|d|...|c|m|m|

m = magic == "fP"
l = packet length
i = Device ID Set
t = event type
l = data length 
d = data bytes
c = 8 bit CRC of all previous bytes
m = magic == "fP"

### Event Types

0.   HALT (safely halt - do not process any event packets unless they are a RESET)
1.   RESET (resume normal processing of packets)
2.   SPARK (turn on sparker for 2-byte millisecond duration)
3.   SOLENOID (open solenoid valve for 2-byte millisecond duration)
4.   PUFF (start a puff sequence)
5.   DISPLAY (display a string)

## Copyrights & Licenses

All code is distributed under the terms of the GNU GPL version 3 with the exception of those files and sections listed below.

### crc.h & crc.c

These are adapted from the source of the BertOS operating system [1], and are distributed under the terms of the GNU GPL version 2.

[1] https://github.com/develersrl/bertos/
