from cube2common.constants import client_states
from spyd.registry_manager import register


@register('room_player_event_handler')
class SuicideHandler(object):
    event_type = 'suicide'

    @staticmethod
    def handle(room, player):
        player.state.state = client_states.CS_DEAD
        room.gamemode.on_player_death(player, player)
        room._broadcaster.player_died(player, player)
