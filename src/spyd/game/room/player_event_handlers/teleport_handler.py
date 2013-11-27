from spyd.registry_manager import register


@register('room_player_event_handler')
class TeleportHandler(object):
    event_type = 'teleport'

    @staticmethod
    def handle(room, player, teleport, teledest):
        room._broadcaster.teleport(player, teleport, teledest)
