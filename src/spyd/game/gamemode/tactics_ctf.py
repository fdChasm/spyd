from cube2common.constants import armor_types
from spyd.game.gamemode.bases.ctf_base import CtfBase
from spyd.game.gamemode.bases.fighting_base import FightingBase
from spyd.game.gamemode.bases.mode_base import ModeBase
from spyd.game.gamemode.bases.spawning_base import SpawningBase
from spyd.game.gamemode.bases.tactics_base import TacticsBase
from spyd.game.gamemode.bases.spectating_base import SpectatingBase
from spyd.registry_manager import register


@register('gamemode')
class TacticsCtf(ModeBase, CtfBase, FightingBase, TacticsBase, SpawningBase, SpectatingBase):
    isbasemode = False
    clientmodename = 'tacctf'
    clientmodenum = 17
    timed = True
    timeout = 600
    hasitems = False
    hasflags = True
    hasteams = True
    spawnarmour = 100
    spawnarmourtype = armor_types.A_GREEN
    spawnhealth = 100
    spawndelay = 5
    hasbases = False
