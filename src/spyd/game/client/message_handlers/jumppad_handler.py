from spyd.registry_manager import register


@register('client_message_handler')
class JumppadHandler(object):
    message_type = 'N_JUMPPAD'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('jumppad', player, message['jumppad'])
