from cube2common.constants import weapon_types
from spyd.protocol import swh
from spyd.registry_manager import register
from spyd.utils.constrain import constrain_range


@register('room_player_event_handler')
class GunselectHandler(object):
    event_type = 'gunselect'

    @staticmethod
    def handle(room, player, gunselect):
        constrain_range(gunselect, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        player.state.gunselect = gunselect
        swh.put_gunselect(player.state.messages, gunselect)
