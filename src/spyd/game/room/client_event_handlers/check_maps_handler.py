from spyd.registry_manager import register

@register('room_client_event_handler')
class CheckMapsHandler(object):
    event_type = 'check_maps'

    @staticmethod
    def handle(room, client):
        pass

