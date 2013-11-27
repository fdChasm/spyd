from spyd.registry_manager import register


@register('room_player_event_handler')
class RequestSpawnHandler(object):
    event_type = 'request_spawn'

    @staticmethod
    def handle(room, player):
        room.gamemode.on_player_request_spawn(player)
