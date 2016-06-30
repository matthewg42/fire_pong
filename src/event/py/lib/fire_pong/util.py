import threading
import re

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


