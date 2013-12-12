from spyd.registry_manager import register


@register('client_message_handler')
class ServcmdHandler(object):
    message_type = 'N_SERVCMD'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('command', client, message['command'])
