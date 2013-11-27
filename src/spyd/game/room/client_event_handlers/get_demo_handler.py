from spyd.registry_manager import register

@register('room_client_event_handler')
class GetDemoHandler(object):
    event_type = 'get_demo'

    @staticmethod
    def handle(room, client, demo_id):
        pass

