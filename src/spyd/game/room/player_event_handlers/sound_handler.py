from spyd.protocol import swh
from spyd.registry_manager import register


@register('room_player_event_handler')
class SoundHandler(object):
    event_type = 'sound'

    @staticmethod
    def handle(room, player, sound):
        swh.put_sound(player.state.messages, sound)
