from spyd.registry_manager import register


@register('room_player_event_handler')
class EditFaceHandler(object):
    event_type = 'edit_face'

    @staticmethod
    def handle(room, selection, direction, mode):
        pass
