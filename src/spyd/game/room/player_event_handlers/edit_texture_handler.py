from spyd.registry_manager import register


@register('room_player_event_handler')
class EditTextureHandler(object):
    event_type = 'edit_texture'

    @staticmethod
    def handle(room, selection, texture, all_faces):
        pass
