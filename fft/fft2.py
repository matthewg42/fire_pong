#!/usr/bin/env python2 
import alsaaudio as alsa
import time
import audioop
import math
import time
import numpy as np
import logging
from struct import pack,unpack

log = logging
means = []
meanlen = 15
chunk = 512
sample_rate = 44100
start = time.time()
sensitivity = 0.5 
inp = None
out = None

def main():
    global out, means, inp, sensitivity
    setup()
    while True:
        l,data = inp.read()
        inp.pause(1)
        if l:
            try:
                matrix=calculate_levels(data, chunk, sample_rate)
                s = '%.2f' % (time.time() - start)
                for i in range(0, 8):
                    diff = matrix[i] - means[i].mean()
                    puff = '%10s' % ''
                    if diff > 0:
                        means[i].set(matrix[i])
                        if diff > sensitivity:
                            puff = ('%10s' % ('PUFF%.2f' % diff))
                    else:
                        means[i].push(matrix[i])
                    s += puff
                print s

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
    # Araange array into 8 rows for the 8 bars on LED matrix
    power = np.reshape(power,(8,chunk/8))
    matrix= np.average(power,axis=1)/4
    return matrix

def plot(n, m):
    print('#' * int(100*float(n)/float(m)))

def setup():
    global inp, out, means
    for _ in range(0, 8):
        means.append(RunningMean(meanlen))
        means[-1].set(0)

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
        self.last.append(n)
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
