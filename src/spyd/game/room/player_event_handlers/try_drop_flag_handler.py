from spyd.registry_manager import register


@register('room_player_event_handler')
class TryDropFlagHandler(object):
    event_type = 'try_drop_flag'

    @staticmethod
    def handle(room, player):
        room.gamemode.on_player_try_drop_flag(player)
