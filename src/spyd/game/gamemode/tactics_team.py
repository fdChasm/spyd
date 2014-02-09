from cube2common.constants import armor_types
from spyd.game.gamemode.bases.fighting_base import FightingBase
from spyd.game.gamemode.bases.mode_base import ModeBase
from spyd.game.gamemode.bases.spawning_base import SpawningBase
from spyd.game.gamemode.bases.spectating_base import SpectatingBase
from spyd.game.gamemode.bases.tactics_base import TacticsBase
from spyd.game.gamemode.bases.teamplay_base import TeamplayBase
from spyd.registry_manager import register


@register('gamemode')
class TacticsTeam(ModeBase, FightingBase, TacticsBase, SpawningBase, SpectatingBase, TeamplayBase):
    isbasemode = True
    clientmodename = 'tacteam'
    clientmodenum = 8
    timed = True
    timeout = 600
    hasitems = False
    hasflags = False
    hasteams = True
    spawnarmour = 100
    spawnarmourtype = armor_types.A_GREEN
    spawnhealth = 100
    spawndelay = 0
    hasbases = False
