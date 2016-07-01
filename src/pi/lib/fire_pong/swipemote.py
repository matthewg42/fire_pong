
from threading import Timer
import cwiid
import time
import logging
from fire_pong.scoreboard import ScoreBoard
import fire_pong.util

log = logging

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

class SwipeMote:
    def __init__(self, name, callback):
        self.name = name
        self.last_swipe = 0
        self.last_sample = 0
        self.previous_ys = RunningMean(SwipeMote.SAMPLES)
        self.callback = callback
        self.wm = None

    def discover(self):
        while self.wm is None:
            try:
                print('Put Wiimote for player %s in discovery mode' % self.name)
                #ScoreBoard().display('D%s' % self.name)
                self.wm = cwiid.Wiimote()
                self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
                self.last_swipe = 0
                log.debug('Connected to wiimote for %s' % self.name)
            except RuntimeError as e:
                log.error('%s - run "sudo hciconfig hci0 up"?' % e)
            except Exception as e:
                log.error('While discovering WiiMote %s / %s' % (type(e), e))
                ScoreBoard().display('ER%s' % self.name)
                time.sleep(1.5)
        
    def rumble(self, state):
        try:
            self.wm.rumble = state
        except Exception as e:
            log.error('SwipeMote(%s).rumble(%s) %s', (self.name, self.state, e))

    def tick(self):
        if time.time() - self.last_sample > SwipeMote.RATE_LIMIT:
            self.last_sample = time.time()
            self.previous_ys.push(self.wm.state['acc'][1])
            if time.time() - self.last_swipe > SwipeMote.IDLE and self.previous_ys.all_over(SwipeMote.SWIPE_MIN) :
                self.last_swipe = time.time()
                mean = self.previous_ys.mean()
                strength = (mean-SwipeMote.SWIPE_MIN)*100/(SwipeMote.SWIPE_MAX-SwipeMote.SWIPE_MIN)
                self.rumble(1)
                Timer(0.3, self.rumble, (0,)).start()
                self.callback(self.name, strength)
            
    # don't sample if it has been less than this time since the last sample
    RATE_LIMIT = 0.03

    # min accelerometer reading to register a swipe
    SWIPE_MIN = 170

    # max accelerometer reading to register a swipe (used to calculate strength)
    SWIPE_MAX = 190

    # how long to wait between detecting swipes (in seconds)
    IDLE = 1.5

    # number of samples to use to detect swipes
    SAMPLES = 8

if __name__ == '__main__':
    import fire_pong.scoreboard
    def got(player, strength):
        print('Detected swipe for %s with strength: %s' % (player, strength))

    log.basicConfig(level=logging.DEBUG)
    fire_pong.scoreboard.log = log
    fire_pong.util.set_test_config() 

    sm1 = SwipeMote ('Mouse', got)
    sm2 = SwipeMote ('Ian', got)
    sm1.discover()
    sm2.discover()
    while True:
        sm1.tick()
        sm2.tick()


