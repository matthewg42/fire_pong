#!/usr/bin/env python2

import subprocess
from fire_pong.swipemote import SwipeMote

def play_sample(path, volume):
    cmd = ['play', path]
    subprocess.Popen(cmd)

if __name__ == '__main__':
    # We want to be able detect subsequent events more quickly than the default
    SwipeMote.IDLE=0.3
    # ...and be more sensitive...
    SwipeMote.SWIPE_MIN=150


    sm1 = SwipeMote ('/home/mouse/audio/digits/1.wav', play_sample)
    sm1.discover()
    sm2 = SwipeMote ('/home/mouse/audio/digits/2.wav', play_sample)
    sm2.discover()

    while True:
        sm1.tick()
        sm2.tick()


