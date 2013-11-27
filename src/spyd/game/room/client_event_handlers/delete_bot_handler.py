from spyd.registry_manager import register

@register('room_client_event_handler')
class DeleteBotHandler(object):
    event_type = 'delete_bot'

    @staticmethod
    def handle(room, client):
        pass

