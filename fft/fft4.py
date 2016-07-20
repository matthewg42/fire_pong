#!/usr/bin/env python2 
import alsaaudio as alsa
import time
import audioop
import math
import time
import numpy as np
import logging
import random
from struct import pack,unpack

log = logging
means = []
meanlen = 10
puff_frequency = None
frequencylen = 30
threshold = 1
threshold_step = 0.001
min_threshold = 0.2
max_threshold = 10
target_density = 0.05
puffers = [0x1000, 0x2000, 0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x100, 0x200, 0x400, 0x800]
channels = []
min_wait = 0.5
max_wait = 2.5
chunk = (len(puffers)/2)*80 
sample_rate = 44100
start = time.time()
inp = None
out = None

def main():
    global out, means, inp, puff_frequency, threshold, channels
    setup()
    while True:
        l,data = inp.read()
        inp.pause(1)
        if l:
            try:
                matrix=calculate_levels(data, chunk, sample_rate)
                puffer_state = (len(channels)*2) * ['    ']
                puffcount = 0
                for i in range(0, len(channels)):
                    diff = matrix[i] - means[i].mean()
                    if diff > 0:
                        means[i].set(matrix[i])
                        if diff > threshold:
                            puffer_idx = i*2
                            if channels[i]:
                                puffer_idx += 1
                            channels[i] = not(channels[i])
                            puffer_state[puffer_idx] = 'PUFF'
                            puffcount += 1
                    else:
                        means[i].push(matrix[i])

                puff_frequency.push(puffcount)
                puff_density = puff_frequency.mean()
                if target_density > puff_density and threshold > min_threshold:
                    threshold -= threshold_step
                elif threshold < max_threshold:
                    threshold += threshold_step
                print('t=%5.2f d=%5.3f t=%5.3f | %s' % (
                        time.time() - start,
                        puff_density, 
                        threshold,
                        '  '.join(puffer_state)))
                out.write(data)
            except Exception as e:
                log.exception("END: %s: %s" % (type(e), e))
                break
        inp.pause(0)

"""
def calculate_levels(data, chunk,sample_rate):
    # Convert raw data to numpy array
    data = unpack("%dh"%(len(data)/2),data)
    data = np.array(data, dtype='h')
    # Apply FFT - real data so rfft used
    fourier=np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier=np.delete(fourier,len(fourier)-1)
    # Find amplitude
    power = np.log10(np.abs(fourier))**2
    # Araange array into 8 rows for the 8 bars on LED matrix
    power = np.reshape(power,(8,chunk/8))
    matrix= np.int_(np.average(power,axis=1)/4)
    return matrix
"""

def calculate_levels(data, chunk,sample_rate):
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
    power = np.reshape(power,(len(channels),chunk/len(channels)))
    matrix= np.average(power,axis=1)/4
    return matrix

def plot(n, m):
    print('#' * int(100*float(n)/float(m)))

def setup():
    global inp, out, means, puff_frequency, channels
    for _ in range(0, len(puffers)/2):
        means.append(RunningMean(meanlen))
        means[-1].set(0)
        channels.append(False)

    puff_frequency = RunningMean(frequencylen)

    inp = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, 'hw:Loopback,1,0')
    out = alsa.PCM(alsa.PCM_PLAYBACK, alsa.PCM_NORMAL, 'plughw:0,0')

    inp.setchannels(2)
    inp.setrate(sample_rate)
    inp.setformat(alsa.PCM_FORMAT_S16_LE)
    inp.setperiodsize(chunk)

    out.setchannels(2)
    out.setrate(sample_rate)
    out.setformat(alsa.PCM_FORMAT_S16_LE)
    out.setperiodsize(chunk)

class RunningMean:
    def __init__(self, n): 
        self.n = n 
        self.last = []
    
    def push(self, n): 
        self.last.append(float(n))
        if len(self.last) > self.n:
            self.last.pop(0)

    def mean(self):
        return sum(self.last) / len(self.last)

    def set(self, n):
        self.last = [n]

    def all_over(self, n): 
        for l in self.last:
            if l < n:
                return False
        return True

if __name__ == '__main__':
    main()
