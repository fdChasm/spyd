from spyd.registry_manager import register


@register('client_message_handler')
class TauntHandler(object):
    message_type = 'N_TAUNT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.handle_player_event('taunt', player)
