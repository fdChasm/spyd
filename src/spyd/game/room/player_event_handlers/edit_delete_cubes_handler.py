from spyd.registry_manager import register


@register('room_player_event_handler')
class EditDeleteCubesHandler(object):
    event_type = 'edit_delete_cubes'

    @staticmethod
    def handle(room, selection):
        pass
