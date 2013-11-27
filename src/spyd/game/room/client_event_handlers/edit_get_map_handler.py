from spyd.registry_manager import register

@register('room_client_event_handler')
class EditGetMapHandler(object):
    event_type = 'edit_get_map'

    @staticmethod
    def handle(room, client):
        pass

