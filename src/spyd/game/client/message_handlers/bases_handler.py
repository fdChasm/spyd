from spyd.registry_manager import register


@register('client_message_handler')
class BasesHandler(object):
    message_type = 'N_BASES'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('base_list', client, message['bases'])
