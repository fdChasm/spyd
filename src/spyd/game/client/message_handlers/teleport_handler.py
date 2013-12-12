from spyd.registry_manager import register


@register('client_message_handler')
class TeleportHandler(object):
    message_type = 'N_TELEPORT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('teleport', player, message['teleport'], message['teledest'])
