from spyd.registry_manager import register


@register('client_message_handler')
class GetdemoHandler(object):
    message_type = 'N_GETDEMO'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('get_demo', client, message['demonum'])
