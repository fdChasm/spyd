from spyd.registry_manager import register

@register('room_client_event_handler')
class EditRemipHandler(object):
    event_type = 'edit_remip'

    @staticmethod
    def handle(room, client):
        pass

