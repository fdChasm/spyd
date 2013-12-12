from spyd.registry_manager import register


@register('client_message_handler')
class CleardemosHandler(object):
    message_type = 'N_CLEARDEMOS'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('clear_demo', client, message['demonum'])
