from spyd.registry_manager import register


@register('room_player_event_handler')
class TauntHandler(object):
    event_type = 'taunt'

    @staticmethod
    def handle(room, player):
        room.gamemode.on_player_taunt(player)
