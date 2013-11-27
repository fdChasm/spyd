from spyd.registry_manager import register

@register('room_client_event_handler')
class SetDemoRecordingHandler(object):
    event_type = 'set_demo_recording'

    @staticmethod
    def handle(room, client, value):
        pass

