#!/usr/bin/env python2

import subprocess
import time
import serial
import sys
import struct
import random
from fire_pong.fp_event import FpEvent
from fire_pong.swipemote import SwipeMote

global running
global idx 
global ok_idx

def start_seq(player, strength):
    global running, idx, ok_idx
    if idx in ok_idx:
        play_audio('boing.wav')
        print('POOOIIIINNNNGGG!')
        running = True
        idx = 0
    else:
        game_over()

def play_audio(path):
    cmd = ['play', path]
    subprocess.Popen(cmd)

def game_over():
    global running, idx
    running = False
    idx = -1
    play_audio('explosion.wav')
    for i in range(0, 20):
        print('GAME OVER!')
    time.sleep(5)
    print('OK, try again...')

if __name__ == '__main__':
    global running, idx, ok_idx
    idx = -1
    running = False
    ok_idx = [-1, 6, 7]

    pong_seq = [ 
        FpEvent(0x1, 'FP_EVENT_PUFF', struct.pack('<H', 250)), 
        FpEvent(0x2, 'FP_EVENT_PUFF', struct.pack('<H', 250)), 
        FpEvent(0x4, 'FP_EVENT_PUFF', struct.pack('<H', 250)), 
        FpEvent(0x8, 'FP_EVENT_PUFF', struct.pack('<H', 250)), 
        FpEvent(0x4, 'FP_EVENT_PUFF', struct.pack('<H', 250)), 
        FpEvent(0x2, 'FP_EVENT_PUFF', struct.pack('<H', 250))
    ]

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        #port='/dev/ttyACM0',
        port='/dev/ttyUSB0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    # Open serial comms
    ser.isOpen()

    # Configure WiiMote
    sm = SwipeMote ('Player', start_seq)
    sm.discover()

    # Some state variables
    last = time.time()
        
    while 1:
        if ser.inWaiting() > 0:
            try:
                data = ser.read(1)
                sys.stdout.write(data.decode())
            except UnicodeDecodeError:
                sys.stdout.write('?')
        sm.tick()
        if idx > max(ok_idx):
            game_over()

        if time.time() - last > 0.3 and running:
            print("Sequence number:", idx)
            last = time.time()
            if idx >= 0 and idx < len(pong_seq):
                e = pong_seq[idx]
                print('SEND: %s' % str(e))
                ser.write(e.serialize())
            idx+=1

