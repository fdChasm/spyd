from spyd.registry_manager import register


@register('client_message_handler')
class GamespeedHandler(object):
    message_type = 'N_GAMESPEED'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('set_game_speed', client, message['value'])
