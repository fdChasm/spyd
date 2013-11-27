from spyd.registry_manager import register


@register('room_player_event_handler')
class EditFlipHandler(object):
    event_type = 'edit_flip'

    @staticmethod
    def handle(room, selection):
        pass
