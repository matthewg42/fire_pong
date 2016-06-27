#!/usr/bin/env python2

import logging
import logging.handlers
import os
import re
import serial
import sys
import time
import json
import threading
import fire_pong.fp_event
import fire_pong.scoreboard
import fire_pong.swipemote
import fire_pong.pongmatch
import fire_pong.ponggame
import fire_pong.fp_serial
from fire_pong.pongmatch import PongMatch

global primary_mode
primary_mode = None
global args
global log
global serial_bus
serial_bus = None

def main():
    global args, log, serial_bus, primary_mode
    init_log()
    try:
        config = read_config_file()
        sanity_checks(config)
    except Exception as e:
        log.critical('%s' % e)
        cleanup_and_exit(1)
    log.info('main() start, daemon=%s, pid-file=%s' % (args.daemon, args.pid_file))

    if args.pid_file is not None:
        pid = str(os.getpid())
        if os.path.isfile(args.pid_file):
            log.critical("PID file %s already exists, aborting" % args.pid_file)
            sys.exit(3)
        else:
            open(args.pid_file, 'w').write(pid)

    # Open serial connection
    try:
        serial_bus = fire_pong.fp_serial.open_serial(config)
    except Exception as e:
        log.critical("Failed to open serial bus: %s" % e)
        cleanup_and_exit(4)

    try:
        primary_mode = PongMatch(config, serial_bus)
    except Exception as e:
        log.exception('Failed to create PongMatch: %s' % e)
        cleanup_and_exit(2)
    primary_mode.run()
    log.info('main() end')
    cleanup_and_exit(0)

def read_config_file():
    """ Reads configuration file and returns a dict with configuration in """
    global args, log
    if not os.path.exists(args.config_file):
        create_default_config_file()
    with open(args.config_file) as json_file:
        config = json.load(json_file)
    config['config_file_path'] = args.config_file
    if args.serial_device:
        config['serial']['port'] = args.serial_device
    log.debug('config: %s' % config)
    return config

def create_default_config_file():
    # The default config file is kept in /opt/firepong/share/firepong.json
    log.debug('create_default_config_file()')
    template_path = get_template_config_path()
    try:
        log.info('Copying default config file: %s -> %s' % (template_path, args.config_file))
        with open(template_path, 'r') as infile, open(args.config_file, 'w') as outfile:
            for line in infile.readlines():
                outfile.write(re.sub(r'\"id\"\s*:\s*\"COMMSHUBID\"', '"id": "%s"' % commshub_id, line))
    except Exception as e:
        log.exception('While copying default config file: %s' % e)

def get_template_config_path():
    try:
        root_path = os.environ['FIREPONG_ROOT']
    except:
        log.warning('FIREPONG_ROOT environment variable not set, trying to determine template config path from binary path')
        root_path = os.path.dirname(sys.argv[0]) + '/../'
    return root_path.rstrip('/') + '/etc/firepong.json'

def sanity_checks(config):
    # If there are any compulsorary config file argss... check here and
    # raise exceptions on failures. 
    pass 

def init_log():
    """ Initialize the log - use syslog if running as a daemon """
    global args, log
    program = os.path.basename(sys.argv[0])
    if args.daemon:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        fmt = '%s[%%(process)d] %%(levelname)s: %%(message)s' % program
    else:
        handler = logging.StreamHandler()
        fmt = ""
        if args.log_timestamps:
            fmt += '%%(asctime)s %s[%%(process)d] ' % program
        fmt += '%(levelname)s: %(message)s'
    handler.setFormatter(logging.Formatter(fmt))
    log = logging.getLogger('firepong')
    log.setLevel(args.logging_level)
    log.addHandler(handler)
    # Set logging in our various modules to use our new logger. These 
    # hoops brought to you by the combination of daemon and logging 
    # modules
    fire_pong.swipemote.log = log
    fire_pong.scoreboard.log = log
    fire_pong.fp_event.log = log
    fire_pong.pongmatch.log = log
    fire_pong.ponggame.log = log

def cleanup_and_exit(level):
    """ Remove PID file and exit the process """
    global log, args
    if args.pid_file is not None:
        if os.path.exists(args.pid_file):
            os.unlink(args.pid_file)
    sys.exit(level)

def sighandler(signum, frame):
    """ Shut down gracefully """
    global log, primary_mode
    if signum in (signal.SIGINT, signal.SIGQUIT, signal.SIGTERM):
        log.info('sighandler() received signal %s, shutting down...' % signum)
        if primary_mode:
            log.info('sighandler() calling shutdown() for sensor_manager')
            primary_mode.shutdown()
    elif signum == signal.SIGHUP:
        log.info('sighandler() received signal HUP, reloading config')
        try:
            config = read_config_file()
            sanity_checks(config)
        except Exception as e:
            log.error('while loading config file: %s' % e)
            return(1)
        sensor_manager.apply_config(config)   
    elif signum == signal.SIGUSR1:
        log.info('sighandler() received signal USR1, rescanning RS485 bus')
        sensor_manager.request_scan_bus()
    else:
        log.info('sighandler() received signal %s, not used at present - ignoring' % signum)
    
if __name__ == '__main__':
    import argparse
    import signal
    import daemon

    global args

    parser = argparse.ArgumentParser(description='Fire Pong')
    parser.add_argument('-c', '--config-file', dest='config_file', 
        default='/etc/firepong.json', 
        help='specify the path to the config file')
    parser.add_argument('-D', '--serial-device', dest='serial_device', 
        default=None, 
        help='over-ride config file serial device')
    parser.add_argument('--pid-file', dest='pid_file', default=None, 
        help='specify path to a PID file to create while running')
    parser.add_argument('-d', '--daemon', dest='daemon', action='store_const',
        const=True, default=False, 
        help='run in daemon mode (detach, log to syslog)')
    parser.add_argument('--debug', dest='logging_level', action='store_const',
        const=logging.DEBUG, default=logging.WARN, 
        help='write debugging output in the log')
    parser.add_argument('--info', dest='logging_level', action='store_const',
        const=logging.INFO, help='write informational output in the log')
    parser.add_argument('--log-ts', dest='log_timestamps', 
        action='store_const', const=True, default=False, 
        help='write informational output in the log')
    args = parser.parse_args()

    for sig in [signal.SIGHUP, 
                signal.SIGUSR1, 
                signal.SIGUSR2,
                signal.SIGTERM, 
                signal.SIGQUIT, 
                signal.SIGINT]:
        signal.signal(sig, sighandler)

    if args.daemon:
        with daemon.DaemonContext(umask=0o022):
            main()
    else:
        main()

