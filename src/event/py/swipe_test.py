#!/usr/bin/env python2

import cwiid
import time
from threading import Timer

SWIPE_MIN = 170
SWIPE_MAX = 190
SWIPE_IDLE = 0.15
SWIPE_DELAY = 0.01
SWIPE_SAMPLES = 12

global last_swipes
global wiimotes
global previous_ys

class RunningMean:
    def __init__(self, n): 
        self.n = n 
        self.last = []
    
    def push(self, n): 
        self.last.append(n)
        if len(self.last) > self.n:
            self.last.pop(0)

    def mean(self):
        return sum(self.last) / len(self.last)

    def all_over(self, n):
        for l in self.last:
            if l < n:
                return False
        return True

def connect_wiimote(wid):
    global wiimotes
    print("Put WiiMote for %s in discovery mode..." % wid)
    try:
        wm = cwiid.Wiimote()
        wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        wiimotes[wid] = wm
        last_swipes[wid] = 0
        previous_ys[wid] = RunningMean(SWIPE_SAMPLES)
        print('Connected to wiimote for %s' % wid)
    except RuntimeError as e: 
        print(e)

def acc2bar(n, length=21, minimum=-3, maximum=3):
    chars = ['-'] * length
    center = length/2
    chars[center] = '|' 
    if n>0:
        for i in range(1, (n*(length-center)/maximum)):
            i += center
            if i < length:
                chars[i] = '#' 
    elif n<0:
        for i in range(-1, 0-(abs(n)*(length-center)/abs(minimum)), -1):
            i += center
            if i >= 0:
                chars[i] = '#' 
    return ''.join(chars)

def rumble(player, state):
    global wiimotes
    wiimotes[player].rumble = state
        
if __name__ == '__main__':
    global wiimotes, last_swipes
    wiimotes = dict()
    last_swipes = dict()
    previous_ys = dict()
    #players = ['Ian', 'Mouse']
    players = ['Mouse']
    for player in players:
        while player not in wiimotes:
            connect_wiimote(player)
    while True:
        for player in players:
            previous_ys[player].push(wiimotes[player].state['acc'][1])
            if previous_ys[player].all_over(SWIPE_MIN) and time.time() - last_swipes[player] > SWIPE_IDLE:
                mean = previous_ys[player].mean()
                swipe_strength = (mean-SWIPE_MIN)*100/(SWIPE_MAX-SWIPE_MIN)
                print 'Swipe detected by %s, strength=%s [%s]' % (player, swipe_strength, previous_ys[player].last)
                rumble(player, 1)
                Timer(0.3, rumble, (player, 0)).start()
                last_swipes[player] = time.time()
        time.sleep(SWIPE_DELAY)
