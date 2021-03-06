import threading
import re
import os
import json

log = None

config = {}

def tid():
    """ Return a string identifier for the current thread """
    return threading.currentThread().getName()

def tid_num():
    """ Return a numerical identifier for the current thread """
    n = re.sub(r'[^\d]', r'', tid())
    if n == '':
        return 0
    else:
        return int(n)

def load_config(args):
    global config
    """ Reads configuration file and sets the config (module variable) """
    if not os.path.exists(args.config_file):
        raise Exception('config file not readable: %s' % args.config_file)
    with open(args.config_file) as json_file:
        config = json.load(json_file)
    config['config_file_path'] = args.config_file
    if args.serial_device:
        config['serial']['port'] = args.serial_device
    if 'serial' not in config:
        config['serial'] = dict()
    if args.serial_debug is not None:
        config['serial']['debug'] = args.serial_debug
    log.debug('load_config: config=%s' % config)

def set_test_config():
    global config
    config = {
        "serial": {
            "doc": "Serial port parameters - these must match what is baked into the Arduino firmwares",
            "port": "/dev/ttyUSB0",
            "baudrate": 115200,
            "parity": "none",
            "stopbits": 2,
            "bytesize": 8,
            "debug": False
        },
        "ModeManager": {
            "doc": "Settings for the ModeManager",
            "tick": 0.5
        },
        "InputManager": {
            "doc": "Settings for the InputManager (buttons and wiimote setup)",
            "tick": 0.02,
            "wiimotes": {
                "enabled": True,
                "swipe_idle": 1,
                "swipe_min": 150
            },
            "gpio": {
                "enabled": False,
                "start": 4,
                "emstop": 5,
                "back": 6
            },
            "keyboard": {
                "tick": 0.02,
                "enabled": True,
                "start": "s",
                "emstop": "h",
                "back": "b",
                "swipe1": "z",
                "swipe2": "COMMA"
            }
        },
        "PongMatch": {
            "doc": "Match specific settings",
            "winning_score": 3
        },
        "PongGame": {
            "puffers": [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048],
            "initial_delay": 0.4
        },
        "LargePuffers": {
            "ids": [4096, 8192]
        },
        "display": {
            "id": 16384
        }
    }
