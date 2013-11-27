from spyd.registry_manager import register


@register('room_player_event_handler')
class EditRotateHandler(object):
    event_type = 'edit_rotate'

    @staticmethod
    def handle(room, selection, axis):
        pass
