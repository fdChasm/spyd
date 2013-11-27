from spyd.registry_manager import register


@register('room_player_event_handler')
class TakeFlagHandler(object):
    event_type = 'take_flag'

    @staticmethod
    def handle(room, player, flag, version):
        room.gamemode.on_player_take_flag(player, flag, version)
