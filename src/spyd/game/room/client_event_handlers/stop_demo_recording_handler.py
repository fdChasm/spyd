from spyd.registry_manager import register

@register('room_client_event_handler')
class StopDemoRecordingHandler(object):
    event_type = 'stop_demo_recording'

    @staticmethod
    def handle(room, client):
        pass

