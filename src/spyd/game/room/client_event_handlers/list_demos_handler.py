from spyd.registry_manager import register

@register('room_client_event_handler')
class ListDemosHandler(object):
    event_type = 'list_demos'

    @staticmethod
    def handle(room, client):
        pass

