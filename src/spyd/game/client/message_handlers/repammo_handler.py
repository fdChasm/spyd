from spyd.registry_manager import register


@register('client_message_handler')
class RepammoHandler(object):
    message_type = 'N_REPAMMO'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('replenish_ammo', player)
