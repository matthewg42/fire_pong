import time
import threading
import struct
import re
import subprocess
import alsaaudio as alsa
import audioop
import math
import numpy as np
import random
from os import listdir
from struct import pack, unpack
from fire_pong.util import log, config
from fire_pong.mode import Mode
from fire_pong.scoreboard import ScoreBoard
from fire_pong.events import *
from fire_pong.modemanager import ModeManager
from fire_pong.fp_event import FpEvent
from fire_pong.fp_serial import FpSerial
from fire_pong.menumode import MenuMode
from fire_pong.runningmean import RunningMean

class MusicMode(Mode):
    __displayname__ = 'MM'
    ''' Select a tune to play '''
    def __init__(self):
        Mode.__init__(self)
        self.music_path = config['MusicMode']['path']
        log.debug('MusicMode.__init__() looking in: %s' % self.music_path)
        self.music_files = []
        for f in sorted(listdir(self.music_path)):
            m = re.match(r'^.*\.(mp3|wav|ogg)$', f, re.IGNORECASE)
            if m:
                f = '%s/%s' % (self.music_path, f)
                log.debug('MusicMode: adding file %s' % f)
                self.music_files.append(f)
        self.display = True
        self.activate = False
        self.idx = 0

    def run(self):
        log.debug('MusicMode.run() START')
        while not self.terminate:
            if self.display:
                self.display = False
                log.info('MusicMode.run() SELECTED idx=%d, song=%s' % (self.idx, self.music_files[self.idx]))
                ScoreBoard().display(self.idx)
                next
            if self.activate:
                self.activate = False
                log.info('MusicMode.run() PLAY %s' % self.music_files[self.idx])
                ModeManager().push_mode(MusicPlayMode(self.music_files[self.idx]))
                next
            time.sleep(0.2)
        log.debug('MusicMode.run() END')

    def event(self, event):
        log.debug('MusicMode.event(%s)' % str(event))
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            self.activate = True

        if type(event) is EventSwipe:
            if event.player == '2UP': 
                self.idx = (self.idx + 1) % len(self.music_files)
            else:
                self.idx = (self.idx - 1) % len(self.music_files)
            self.display = True

class MusicPlayMode(Mode):
    __displayname__ = 'MP'
    ''' Play a tune, and puff along with it! '''
    def __init__(self, music_file):
        log.debug('MusicPlayMode.__init__() START')
        Mode.__init__(self)
        # Make sure moc is running
        subprocess.call(["mocp", "-S"])
        self.music_file = music_file
        self.large_puffers = config['LargePuffers']['ids']
        self.small_puffers = config['PongGame']['puffers']
        self.all_puffers = self.large_puffers
        self.all_puffers.extend(self.small_puffers)
        self.puff_duration = config['MusicMode']['puff_duration']
        self.means = []
        self.meanlen = 10
        self.puff_frequency = None
        self.frequencylen = 30
        self.threshold = 0.2 
        self.threshold_step = 0.004
        self.min_threshold = 0.5
        self.max_threshold = 10
        self.target_density = config['MusicMode']['target_density']
        self.channels = []
        self.min_wait = 0.5
        self.max_wait = 2.5
        self.chunk = (len(self.all_puffers)/2)*80 
        self.sample_rate = 44100
        self.start = time.time()
        self.inp = None
        self.out = None
        self.manual_mask = 0

        try:
            for _ in range(0, len(self.all_puffers)/2):
                self.means.append(RunningMean(self.meanlen))
                self.means[-1].set(0)
                self.channels.append(False)

            self.puff_frequency = RunningMean(self.frequencylen)

            self.inp = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, 'hw:Loopback,1,0')
            self.out = alsa.PCM(alsa.PCM_PLAYBACK, alsa.PCM_NORMAL, 'plughw:0,0')

            self.inp.setchannels(2)
            self.inp.setrate(self.sample_rate)
            self.inp.setformat(alsa.PCM_FORMAT_S16_LE)
            self.inp.setperiodsize(self.chunk)

            self.out.setchannels(2)
            self.out.setrate(self.sample_rate)
            self.out.setformat(alsa.PCM_FORMAT_S16_LE)
            self.out.setperiodsize(self.chunk)
        except Exception as e:
            log.error('MusicPlayMode.__init__() %s: %s' % (type(e), e))
            if self.inp:
                self.inp.close()
            if self.oup:
                self.out.close()
        log.debug('MusicPlayMode.__init__() END')

    def run(self):
        log.debug('MusicPlayMode.run() START')
        time.sleep(0.5)
        try:
            self.start_playback()
            while not self.terminate:
                l, data = self.inp.read()
                self.inp.pause(1)
                if l:
                    try:
                        matrix = self.calculate_levels(data)
                        puffer_state = (len(self.channels)*2) * ['    ']
                        puffcount = 0
                        puffmask = 0x00000000
                        for i in range(0, len(self.channels)):
                            diff = matrix[i] - self.means[i].mean()
                            if diff > 0:
                                self.means[i].set(matrix[i])
                                if diff > self.threshold:
                                    puffer_idx = i*2
                                    if self.channels[i]:
                                        puffer_idx += 1
                                    self.channels[i] = not(self.channels[i])
                                    puffer_state[puffer_idx] = 'PUFF'
                                    puffmask = puffmask | self.all_puffers[puffer_idx]
                                    puffcount += 1
                            else:
                                self.means[i].push(matrix[i])

                        self.puff_frequency.push(puffcount)
                        puff_density = self.puff_frequency.mean()
                        if self.target_density > puff_density and self.threshold > self.min_threshold:
                            self.threshold -= self.threshold_step
                        elif self.threshold < self.max_threshold:
                            self.threshold += self.threshold_step
                        log.debug('t=%5.2f d=%5.3f t=%5.3f | %s' % (
                                time.time() - self.start,
                                puff_density, 
                                self.threshold,
                                '  '.join(puffer_state)))
                        if puffmask != 0:
                            e = FpEvent(puffmask, 'FP_EVENT_PUFF', pack('<H', self.puff_duration))
                            log.info('PUFF event: %s' % str(e))
                            FpSerial().write(e.serialize())
                        self.out.write(data)
                    except Exception as e:
                        log.exception("END: %s: %s" % (type(e), e))
                        break
                self.inp.pause(0)
            self.stop_playback()
        finally:
            try:
                self.inp.close()
                self.oup.close()
            except Exception as e:
                log.error('while closing ALSA devices %s: %s' % (type(e), e))
        log.debug('MusicPlayMode.run() END')

    def start_playback(self):
        # Ensure mixer level is good
        subprocess.call(['amixer', '-q', 'set', 'PCM', '95%'])
        # Clear the queue
        subprocess.call(['mocp', '-c', self.music_file])
        # Enqueue the track 
        subprocess.call(['mocp', '-q', self.music_file])
        # Start playback
        subprocess.call(['mocp', '-p', self.music_file])
 
    def stop_playback(self):
        subprocess.call(['mocp', '-s', self.music_file])
        
    def calculate_levels(self, data):
        # Convert raw data to numpy array
        data = unpack("%dh"%(len(data)/2),data)
        data = np.array(data, dtype='h')
        # Apply FFT - real data so rfft used
        fourier=np.fft.rfft(data)
        # Remove last element in array to make it the same size as chunk
        fourier=np.delete(fourier,len(fourier)-1)
        # Find amplitude
        power = np.log10(np.abs(fourier))**2
        # Araange array into len(channels) frequency bands
        power = np.reshape(power,(len(self.channels), self.chunk/len(self.channels)))
        matrix= np.average(power,axis=1)/4
        return matrix

    def event(self, event):
        if event == EventQuit():
            self.terminate = True

        if event == EventButton('start'):
            self.manual_mask = self.manual_mask | self.small_puffers[random.randint(0, len(self.small_puffers)-1)]

        if type(event) is EventSwipe:
            if event.player == '2UP': 
                self.manual_mask = self.manual_mask | self.large_puffers[0]
            else:
                self.manual_mask = self.manual_mask | self.large_puffers[-1]


