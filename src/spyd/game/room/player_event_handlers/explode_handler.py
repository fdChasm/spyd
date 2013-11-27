from cube2common.constants import weapon_types
from spyd.registry_manager import register
from spyd.utils.constrain import constrain_range


@register('room_player_event_handler')
class ExplodeHandler(object):
    event_type = 'explode'

    @staticmethod
    def handle(room, player, cmillis, gun, explode_id, hits):
        constrain_range(gun, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        room.gamemode.on_player_explode(player, cmillis, gun, explode_id, hits)
