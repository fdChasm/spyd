from spyd.registry_manager import register


@register('client_message_handler')
class DelbotHandler(object):
    message_type = 'N_DELBOT'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('delete_bot', client)
