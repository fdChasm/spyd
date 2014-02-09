from cube2common.constants import armor_types, weapon_types
from spyd.game.gamemode.bases.fighting_base import FightingBase
from spyd.game.gamemode.bases.mode_base import ModeBase
from spyd.game.gamemode.bases.spawning_base import SpawningBase
from spyd.game.gamemode.bases.spectating_base import SpectatingBase
from spyd.game.gamemode.bases.teamplay_base import TeamplayBase
from spyd.registry_manager import register


@register('gamemode')
class InstaTeam(ModeBase, FightingBase, SpawningBase, SpectatingBase, TeamplayBase):
    isbasemode = True
    clientmodename = 'instateam'
    clientmodenum = 4
    timed = True
    timeout = 600
    hasitems = False
    hasflags = False
    hasteams = True
    hasbases = False
    spawnarmour = 0
    spawnarmourtype = armor_types.A_BLUE
    spawnhealth = 1
    spawndelay = 0

    @property
    def spawnammo(self):
        ammo = [0] * weapon_types.NUMGUNS
        ammo[weapon_types.GUN_FIST] = 1
        ammo[weapon_types.GUN_RIFLE] = 100
        return ammo

    spawngunselect = weapon_types.GUN_RIFLE
