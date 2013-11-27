from spyd.registry_manager import register

@register('room_client_event_handler')
class EditNewMapHandler(object):
    event_type = 'edit_new_map'

    @staticmethod
    def handle(room, client, size):
        pass

