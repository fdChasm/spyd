from spyd.registry_manager import register


@register('room_player_event_handler')
class EditMaterialHandler(object):
    event_type = 'edit_material'

    @staticmethod
    def handle(room, selection, material, material_filter):
        pass
