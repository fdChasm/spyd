from spyd.registry_manager import register


@register('client_message_handler')
class EditmodeHandler(object):
    message_type = 'N_EDITMODE'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.handle_player_event('edit_mode', player, message['value'])
