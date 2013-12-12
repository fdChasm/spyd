from spyd.registry_manager import register


@register('client_message_handler')
class PosHandler(object):
    message_type = 'N_POS'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['clientnum'])
        player.state.update_position(message['position'], message['raw_position'])
