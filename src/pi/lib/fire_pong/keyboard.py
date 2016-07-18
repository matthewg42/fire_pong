import pygame
import threading
import time
import os

import fire_pong.util 
from fire_pong.util import log

# Follows the singleton pattern
class Keyboard:
    COLBG =   (150, 0,   0  )
    COLFONT = (210, 210, 210)
    FONTSIZE = 450
    FONTOFFSET = (100,100)

    class __Keyboard:
        def __init__(self):
            self.thread = threading.Thread(target=self.run)
            self.terminate = False
            self.buttons = dict()
            self.pressed = dict()
            self.gain_action = None
            self.screen = None
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

        def init_display(self):
            disp_no = os.getenv("DISPLAY")
            if disp_no:
                log.info('Using X with DISPLAY: %s' % disp_no)
                self.screen = pygame.display.set_mode((800,600))
                pygame.init()
                pygame.font.init()
                pygame.display.set_caption('Fire Pong Keyboard Input')
            else:
                found = False
                drivers = ['fbcon', 'directfb', 'svgalib']
                for driver in drivers:
                    if not os.getenv('SDL_VIDEODRIVER'):
                        os.putenv('SDL_VIDEODRIVER', driver)
                    try:
                        pygame.display.init()
                    except pygame.error as e:
                        log.debug('Framebuffer driver %s failed: %s' % (driver, e))
                        continue
                    found = True
                    log.info('Using framebuffer driver: %s' % driver)
                    break
                if not found:
                    raise Exception('No working video driver found')
                size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
                log.info('Display size: %d x %d' % (size[0], size[1]))
                self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
            self.screen.fill(Keyboard.COLBG)
            pygame.font.init()
            self.font = pygame.font.Font(None, Keyboard.FONTSIZE)
            pygame.display.update()

        def run(self):
            self.init_display()
            while not self.terminate:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate = True
                    if event.type == pygame.KEYUP:
                        log.debug('Keyboard KEYUP event: %s' % event)
                        if event.key in self.buttons:
                            log.debug('Keyboard: key %s pressed, triggering action %s' % (event.key, self.buttons[event.key]))
                            self.pressed[self.buttons[event.key]] = True       
                        if event.scancode == 115:
                            log.debug('Keyboard: btbutton 115 scancode, triggering action %s' % self.gain_action)
                            self.pressed[self.gain_action] = True
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

        def display_text(self, text):
            ''' display a string, centred and big enough to fill the display '''
            if self.screen:
                self.screen.fill(Keyboard.COLBG)
                self.screen.blit(self.font.render(text, 1, Keyboard.COLFONT), Keyboard.FONTOFFSET)
                pygame.display.update()

    instance = None

    def __init__(self):
        if not Keyboard.instance:
            Keyboard.instance = Keyboard.__Keyboard()
        
    def __getattr__(self, name):
        return getattr(self.instance, name)

if __name__ == '__main__':
    import time
    import logging
    log = logging
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
    for _ in range(0, 60):
        if k.get_pressed('quit'):
            break
        else:
            time.sleep(0.1)
    k.shutdown()
    k.thread.join()


