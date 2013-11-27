from spyd.registry_manager import register


@register('room_player_event_handler')
class JumppadHandler(object):
    event_type = 'jumppad'

    @staticmethod
    def handle(room, player, jumppad):
        room._broadcaster.jumppad(player, jumppad)
