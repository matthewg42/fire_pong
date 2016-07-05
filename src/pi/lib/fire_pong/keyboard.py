import pygame
import logging
import threading
import pygame
import time

import fire_pong.util 

log = logging

# Follows the singleton pattern
class Keyboard:
    class __Keyboard:
        def __init__(self):
            self.thread = threading.Thread(target=self.run)
            self.terminate = False
            self.buttons = dict()
            self.pressed = dict()
            self.gain_action = None
            for action in ['quit', 'start', 'emstop', 'back', 'swipe1', 'swipe2', 'btstart', 'btemstop']:
                try:
                    key = fire_pong.util.config['InputManager']['keyboard'][action]
                    if action[0:2] == 'bt':
                        action = action[2:]
                    if key == '_gain':
                        self.gain_action = action
                        log.debug('Keyboard() for _gain input, action is: %s' % action)
                    else:
                        pygame_id = 'K_' + key
                        self.buttons[getattr(pygame, pygame_id)] = action
                        log.debug('Keyboard() for %s input set to key %s' % (action, pygame_id))
                    self.pressed[action] = False
                except KeyError as e:
                    log.warning('Keyboard.__init__(): %s' % e)
                    pass

        def run(self):
            pygame.init()
            gameDisplay = pygame.display.set_mode((800,600))
            pygame.display.set_caption('Fire Pong Keyboard Input')
            while not self.terminate:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate = True
                    if event.type == pygame.KEYUP:
                        if event.key in self.buttons:
                            log.debug('Keyboard: key %s pressed, triggering action %s' % (event.key, self.buttons[event.key]))
                            self.pressed[self.buttons[event.key]] = True       
                        else:
                            log.debug('Keyboard: button not bound: %s' % event)
                    elif self.gain_action is not None and event.type == pygame.ACTIVEEVENT and event.state == 2 and event.gain == 1:
                        log.debug('Keyboard: _gain pressed, triggering action %s' % self.gain_action)
                        self.pressed[self.gain_action] = True
                    
                time.sleep(fire_pong.util.config['InputManager']['keyboard']['tick'])
            pygame.quit() 

        def get_actions(self):
            a = self.pressed.keys()
            if self.gain_action:
                a.append(self.gain_action)
            return a

        def get_pressed(self, action):
            if action not in self.pressed:
                log.warning('Keyboard.get_pressed: requested action %s, but it is not defined in the keyboard settings' % action)
                return False
            if self.pressed[action]:
                self.pressed[action] = False
                return True
            else:
                return False
            
        def shutdown(self):
            self.terminate = True

    instance = None

    def __init__(self):
        if not Keyboard.instance:
            Keyboard.instance = Keyboard.__Keyboard()
        
    def __getattr__(self, name):
        return getattr(self.instance, name)

if __name__ == '__main__':
    import time
    fire_pong.util.config = {
        "InputManager": {
            "tick": 0.02,
            "keyboard": {
                "tick": 0.02,
                "enabled": True,
                "quit": "ESCAPE",
                "start": "s",
                "emstop": "h",
                "back": "b",
                "swipe1": "z",
                "swipe2": "COMMA",
                "btstart": "RETURN",
                "btemstop": "_gain"
            }
        }
    }
    log.basicConfig(level=logging.DEBUG)
    k = Keyboard()
    log.debug('supported actions: %s' % k.get_actions())
    k.thread.start()
    while True:
        if k.get_pressed('quit'):
            break
        else:
            time.sleep(0.1)
    k.shutdown()
    k.thread.join()


