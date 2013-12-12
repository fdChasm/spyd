from spyd.registry_manager import register


@register('client_message_handler')
class GunselectHandler(object):
    message_type = 'N_GUNSELECT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('gunselect', player, message['gunselect'])
