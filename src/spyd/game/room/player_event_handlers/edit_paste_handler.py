from spyd.registry_manager import register


@register('room_player_event_handler')
class EditPasteHandler(object):
    event_type = 'edit_paste'

    @staticmethod
    def handle(room, selection):
        pass
