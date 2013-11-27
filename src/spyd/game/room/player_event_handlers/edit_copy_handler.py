from spyd.registry_manager import register


@register('room_player_event_handler')
class EditCopyHandler(object):
    event_type = 'edit_copy'

    @staticmethod
    def handle(room, selection):
        pass
