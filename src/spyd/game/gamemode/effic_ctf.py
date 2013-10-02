from cube2common.constants import armor_types, weapon_types
from spyd.game.gamemode.bases.ctf_base import CtfBase
from spyd.game.gamemode.bases.fighting_base import FightingBase
from spyd.game.gamemode.bases.mode_base import ModeBase
from spyd.game.gamemode.bases.spawning_base import SpawningBase
from spyd.game.registry_manager import register


@register('gamemode')
class EfficCtf(ModeBase, CtfBase, FightingBase, SpawningBase):
    isbasemode = True
    clientmodename = 'efficctf'
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

    @property
    def spawnammo(self):
        ammo = [0] * weapon_types.NUMGUNS
        ammo[weapon_types.GUN_CG] = 20
        ammo[weapon_types.GUN_SG] = 20
        ammo[weapon_types.GUN_GL] = 20
        ammo[weapon_types.GUN_RL] = 10
        ammo[weapon_types.GUN_RIFLE] = 10
        return ammo

    spawngunselect = weapon_types.GUN_CG
