import random

from cube2common.constants import weapon_types, itemstats


tactics_weapons = (weapon_types.GUN_SG, weapon_types.GUN_CG, weapon_types.GUN_RL, weapon_types.GUN_RIFLE, weapon_types.GUN_GL)

def baseammo(ammo, gun, k=2, scale=1):
    ammo[gun] = (itemstats[gun - weapon_types.GUN_SG].add * k) / scale

class TacticsBase(object):
    def __init__(self, room, map_meta_data):
        self.room = room

    def spawn_loadout(self, player):
        player.state.health = self.spawnhealth
        player.state.armour = self.spawnarmour
        player.state.armourtype = self.spawnarmourtype

        ammo = [0] * weapon_types.NUMGUNS

        gun1, gun2 = random.sample(tactics_weapons, 2)

        baseammo(ammo, gun1, 2)
        baseammo(ammo, gun2, 2)

        ammo[weapon_types.GUN_GL] += 1

        player.state.gunselect = gun1
        player.state.ammo = ammo
