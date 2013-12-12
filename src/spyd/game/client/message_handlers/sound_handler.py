from spyd.registry_manager import register


@register('client_message_handler')
class SoundHandler(object):
    message_type = 'N_SOUND'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('sound', player, message['sound'])
