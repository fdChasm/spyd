from spyd.registry_manager import register

@register('room_client_event_handler')
class ClearDemoHandler(object):
    event_type = 'clear_demo'

    @staticmethod
    def handle(room, client, demo_id):
        pass

