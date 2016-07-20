from textwrap import wrap
import bluepy.btle as btle
from bluepy.btle import Peripheral, UUID

btle.Debugging = True
global de, addr
addr = '18:7A:93:02:7C:5E'
de = None

def dirt(thing):
    print('THING:   %s' % thing)
    print('DOC:     %s' % thing.__doc__)
    print('TYPE:    %s' % type(thing))
    print('STR:     %s' % str(thing))
    a = wrap(str(dir(thing)), 120)
    print('DIR:     %s' % a[0])
    for l in a[1:]:
        print('         %s' % l)

def lss():
    global de
    for u, s in de.services.items():
        print('%s : %s' % (str(u), str(s)))

def service(uuid):
    global de
    for u, s in de.services.items():
        if u == uuid:
            return s
    print('no such service uuid: %s' % uuid)
    return None

def lsc(serv):
    for c in serv.getCharacteristics():
        print('handle=%-3s valHandle=%-3s supportsRead=%-5s uuid=%s properties=%s' % (
                c.handle,
                c.valHandle,
                c.supportsRead(),
                str(c.uuid),
                c.propertiesToString()))

def handler(handle, data):
    print('handler(handle=%s, data=%s)' % (repr(handle), repr(data)))
    
print('connecting to %s...' % addr)
de = Peripheral(addr)
print('connected, discovering services...')
de.discoverServices()
print('commands:')
print('  lss()            list services')
print('  service(uuid)    get service object')
print('  lsc(service)     list characteristics for a service')
print('  char(serv, uuid) get a characteristic by uuid')


