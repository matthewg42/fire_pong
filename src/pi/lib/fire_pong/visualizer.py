from fire_pong.util import log, config
from fire_pong.fp_event import FpEvent

# Follows the singleton pattern
class Visualizer:
    class __Visualizer:
        def __init__(self):
            log.debug('Visualizer.__init__()')
            self.text = ''

        def update(self, event):
            ''' don't display the output '''
            self.as_lines(event)

        def info(self, event):
            for l in self.as_lines(event):
                log.info(l)

        def as_lines(self, event):
            if FpEvent.FP_TYPES[event.fp_type] is 'FP_EVENT_DISPLAY' and event.id_set & config['display']['id'] > 0:
                self.text = str(event.data)

            lines = 5 * ['']

            lines[0] += '  @  ' if self.p4id(config['LargePuffers']['ids'][0], event) else '     '
            lines[1] += '  @  ' if self.p4id(config['LargePuffers']['ids'][0], event) else '     '
            lines[2] += '  |  '
            lines[3] += '  0  '
            lines[4] += ('%04X ' % config['LargePuffers']['ids'][0])

            for pid in config['PongGame']['puffers']:
                lines[0] += '     '
                lines[1] += '  @  ' if self.p4id(pid, event) else '     '
                lines[2] += '  @  ' if self.p4id(pid, event) else '     '
                lines[3] += '  |  '
                lines[4] += ('%04X ' % pid)

            lines[0] += '  @  ' if self.p4id(config['LargePuffers']['ids'][-1], event) else '     '
            lines[1] += '  @  ' if self.p4id(config['LargePuffers']['ids'][-1], event) else '     '
            lines[2] += '  |  '
            lines[3] += '  0  '
            lines[4] += ('%04X ' % config['LargePuffers']['ids'][-1])

            lines[1] += ('"%s"' % self.text)
            
            return lines

        def p4id(self, pid, event):
            return FpEvent.FP_TYPES[event.fp_type] in ['FP_EVENT_PUFF', 'FP_EVENT_ALTPUFF'] and event.id_set & pid > 0

    instance = None

    def __init__(self):
        if not Visualizer.instance:
            Visualizer.instance = Visualizer.__Visualizer()
        
    def __getattr__(self, name):
        return getattr(self.instance, name)



