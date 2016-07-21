#!/usr/bin/env python2

morse = '..- --- --.. .-.. ...'
ml = list(morse)

print(morse)
while len(ml) > 0:
    chunk = ml.pop(0)
    while len(morse) > 0 and ml[0] == chunk[-1]:
        chunk += ml.pop(0)
    print('chunk:', chunk)

