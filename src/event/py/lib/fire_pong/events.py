import logging
import time

log = logging

class Event(object):
    def __init__(self):
        self.time = time.time()
    def __str__(self):
        return 'Event@%.3f' % self.time

class EventQuit(Event):
    def __init__(self):
        Event.__init__(self)
    def __str__(self):
        return 'EventQuit@%.3f' % self.time
    def __eq__(self, other):
        return type(other) is EventQuit

class EventMessage(Event):
    def __init__(self, message):
        Event.__init__(self)
        self.message = message
    def __str__(self):
        return 'EventMessage@%.3f (message=%s)' % (self.time, self.message)
    def __eq__(self, other):
        return type(other) is EventMessage and self.message == other.message

class EventSwipe(Event):
    def __init__(self, player_id, swipe_strength):
        Event.__init__(self)
        self.player_id = player_id
        self.swipe_strength = swipe_strength
    def __str__(self):
        return 'EventSwipe@%.3f (player_id=%s, swipe_strength=%s)' % (self.time, self.player_id, self.swipe_strength)
    def __eq__(self, other):
        return type(other) is EventSwipe and self.player_id == other.player_id

class EventButton(Event):
    def __init__(self, button_id):
        Event.__init__(self)
        self.button_id = button_id
    def __str__(self):
        return 'EventButton@%.3f (button_id=%s)' % (self.time, self.button_id)
    def __eq__(self, other):
        return type(other) is EventButton and self.button_id == other.button_id

if __name__ == '__main__':
    log.basicConfig(level=logging.INFO)
    for e in [Event(), EventSwipe('player 1', 100), EventButton('emstop')]:
        log.info('is a EventSwipe: %s; str: %s' % (type(e) is EventSwipe, e))

