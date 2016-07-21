#!/usr/bin/env python2
#
# Makes changes which we want to see on the installed config, but not in the example
# config file...


import json
import sys
import os
import logging
import subprocess

log = logging
log.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    log.error('''Usage:

%s /path/to/configfile.json
''')
    exit(2)

path = sys.argv[1]
if not os.path.exists(path):
    log.error('config file \"%s\" not found' % path)
    exit(3)

with open(path) as json_file:
    config = json.load(json_file)

config['InputManager']['keyboard']['enabled'] = False
config['InputManager']['gpio']['enabled'] = True
config['InputManager']['wiimotes']['enabled'] = True

# Save the original file as a ~ backup
subprocess.call(['mv', path, path + '~'])

# Write the updated config
with open(path, 'w') as json_file:
    json_file.write(json.dumps(config, sort_keys=True, indent=4))


