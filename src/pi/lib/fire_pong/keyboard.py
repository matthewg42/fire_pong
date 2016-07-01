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
            self.start_button = None
            self.emstop_button = None
            self.back_button = None
            self.swipe1_button = None
            self.swipe2_button = None
            self.start = False
            self.emstop = False
            self.back = False
            self.quit = False
            self.swipe1 = False
            self.swipe2 = False
            try:
                self.quit_button = pygame.K_ESCAPE
                log.debug('Keyboard() set quit to ESCAPE key')
                self.start_button = getattr(pygame, 'K_' + fire_pong.util.config['InputManager']['keyboard']['start'])
                log.debug('Keyboard() set start to %s' % fire_pong.util.config['InputManager']['keyboard']['start'])
                self.emstop_button = getattr(pygame, 'K_' + fire_pong.util.config['InputManager']['keyboard']['emstop'])
                log.debug('Keyboard() set emstop to %s' % fire_pong.util.config['InputManager']['keyboard']['emstop'])
                self.back_button = getattr(pygame, 'K_' + fire_pong.util.config['InputManager']['keyboard']['back'])
                log.debug('Keyboard() set back to %s' % fire_pong.util.config['InputManager']['keyboard']['back'])
                self.swipe1_button = getattr(pygame, 'K_' + fire_pong.util.config['InputManager']['keyboard']['swipe1'])
                log.debug('Keyboard() set swipe1 to %s' % fire_pong.util.config['InputManager']['keyboard']['swipe1'])
                self.swipe2_button = getattr(pygame, 'K_' + fire_pong.util.config['InputManager']['keyboard']['swipe2'])
                log.debug('Keyboard() set swipe2 to %s' % fire_pong.util.config['InputManager']['keyboard']['swipe2'])
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
                        terminate = True
                    if event.type == pygame.KEYUP:
                        if event.key == self.quit_button:
                            self.quit = True
                        if event.key == self.start_button:
                            self.start = True
                        elif event.key == self.emstop_button:
                            self.emstop = True
                        elif event.key == self.back_button:
                            self.back = True
                        elif event.key == self.swipe1_button:
                            self.swipe1 = True
                        elif event.key == self.swipe2_button:
                            self.swipe2 = True
                time.sleep(fire_pong.util.config['InputManager']['keyboard']['tick'])
            pygame.quit()            

        def get_start(self):
            if self.start:
                self.start = False
                return True
            else:
                return False

        def get_emstop(self):
            if self.emstop:
                self.emstop = False
                return True
            else:
                return False

        def get_back(self):
            if self.back:
                self.back = False
                return True
            else:
                return False

        def get_quit(self):
            if self.quit:
                self.quit = False
                return True
            else:
                return False

        def get_swipe1(self):
            if self.swipe1:
                self.swipe1 = False
                return True
            else:
                return False

        def get_swipe2(self):
            if self.swipe2:
                self.swipe2 = False
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
                "start": "s",
                "emstop": "h",
                "back": "b",
                "swipe1": "z",
                "swipe2": "COMMA"
            }
        }
    }
    log.basicConfig(level=logging.DEBUG)
    k = Keyboard()
    k.thread.start()
    for _ in range(0,50):
        print('start=%s emstop=%s back=%s' % (k.get_start(), k.get_emstop(), k.get_back()))
        if k.emstop:
            break
        else:
            time.sleep(0.1)
    k.shutdown()
    k.thread.join()


