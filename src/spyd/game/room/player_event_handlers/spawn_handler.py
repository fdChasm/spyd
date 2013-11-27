from cube2common.constants import weapon_types
from spyd.registry_manager import register
from spyd.utils.constrain import constrain_range


@register('room_player_event_handler')
class SpawnHandler(object):
    event_type = 'spawn'

    @staticmethod
    def handle(room, player, lifesequence, gunselect):
        constrain_range(gunselect, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        player.state.on_respawn(lifesequence, gunselect)
