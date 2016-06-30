#!/usr/bin/env python2

import time
from fire_pong.swipemote import SwipeMote

def eh(player, strength):
    delay = 0.6 - (float(strength)/650)
    print ('player=%s  strength=%d  delay=%5.2f' % (player, strength, delay))

wm1 = SwipeMote('1UP', eh)
#wm2 = SwipeMote('2UP', eh)
wm1.discover()
#wm2.discover()

while True:
    wm1.tick()
#    wm2.tick()
    time.sleep(0.02)

