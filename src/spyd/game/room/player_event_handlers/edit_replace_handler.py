from spyd.registry_manager import register


@register('room_player_event_handler')
class EditReplaceHandler(object):
    event_type = 'edit_replace'

    @staticmethod
    def handle(room, selection, texture, new_texture, in_selection):
        pass
