from spyd.registry_manager import register


@register('client_message_handler')
class TryspawnHandler(object):
    message_type = 'N_TRYSPAWN'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('request_spawn', player)
