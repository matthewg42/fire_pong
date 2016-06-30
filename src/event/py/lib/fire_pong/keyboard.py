import pygame
import logging
import threading
import pygame
import time

log = logging

# Follows the singleton pattern
class Keyboard:
    class __Keyboard:
        def __init__(self, config):
            self.config = config
            self.thread = threading.Thread(target=self.run)
            self.terminate = False
            self.start_button = None
            self.emstop_button = None
            self.back_button = None
            self.start = False
            self.emstop = False
            self.back = False
            self.quit = False
            try:
                self.quit_button = pygame.K_ESCAPE
                log.debug('Keyboard() set quit to ESCAPE key')
                self.start_button = getattr(pygame, 'K_' + config['InputManager']['keyboard']['start'])
                log.debug('Keyboard() set start to %s' % config['InputManager']['keyboard']['start'])
                self.emstop_button = getattr(pygame, 'K_' + config['InputManager']['keyboard']['emstop'])
                log.debug('Keyboard() set emstop to %s' % config['InputManager']['keyboard']['emstop'])
                self.back_button = getattr(pygame, 'K_' + config['InputManager']['keyboard']['back'])
                log.debug('Keyboard() set back to %s' % config['InputManager']['keyboard']['back'])
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
                time.sleep(self.config['InputManager']['keyboard']['tick'])
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

        def shutdown(self):
            self.terminate = True

    instance = None

    def __init__(self, config={'InputManager': {'keyboard': {'back': 'b', 'start': 's', 'emstop': 'h'}}}):
        if not Keyboard.instance:
            Keyboard.instance = Keyboard.__Keyboard(config)
        
    def __getattr__(self, name):
        return getattr(self.instance, name)

if __name__ == '__main__':
    import time
    log.basicConfig(level=logging.DEBUG)
    k = Keyboard()
    k.thread.start()
    for _ in range(0,100):
        print('start=%s emstop=%s back=%s' % (k.start, k.emstop, k.back))
        if k.emstop:
            break
        else:
            time.sleep(0.01)
    k.shutdown()
    k.thread.join()


