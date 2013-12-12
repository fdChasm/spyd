from spyd.registry_manager import register


@register('client_message_handler')
class TextHandler(object):
    message_type = 'N_TEXT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.handle_player_event('game_chat', player, message['text'])
