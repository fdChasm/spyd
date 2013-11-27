from cube2common.constants import weapon_types
from spyd.registry_manager import register
from spyd.utils.constrain import constrain_range


@register('room_player_event_handler')
class ShootHandler(object):
    event_type = 'shoot'

    @staticmethod
    def handle(room, player, shot_id, gun, from_pos, to_pos, hits):
        constrain_range(gun, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        room.gamemode.on_player_shoot(player, shot_id, gun, from_pos, to_pos, hits)
