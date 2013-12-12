from spyd.registry_manager import register


@register('client_message_handler')
class PausegameHandler(object):
    message_type = 'N_PAUSEGAME'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('pause_game', client, message['value'])
