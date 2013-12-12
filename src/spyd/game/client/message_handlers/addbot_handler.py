from spyd.registry_manager import register


@register('client_message_handler')
class AddbotHandler(object):
    message_type = 'N_ADDBOT'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('add_bot', client, message['skill'])
