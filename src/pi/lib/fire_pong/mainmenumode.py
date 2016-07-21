from fire_pong.menumode import MenuMode
from fire_pong.pongmode import PongMode, PongVictory
from fire_pong.continuousmode import ContinuousMode
from fire_pong.setupmode import SetupMenuMode
from fire_pong.musicmode import MusicMode
from fire_pong.manualmode import ManualMode

class MainMenuMode(MenuMode):
    ''' Main Menu '''
    def __init__(self):
        MenuMode.__init__(self, [PongMode, SetupMenuMode, ContinuousMode, PongVictory, MusicMode, ManualMode])


