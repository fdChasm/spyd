from spyd.registry_manager import register

@register('room_client_event_handler')
class AddBotHandler(object):
    event_type = 'add_bot'

    @staticmethod
    def handle(room, client, skill):
        pass

