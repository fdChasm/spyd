from spyd.registry_manager import register


@register('client_message_handler')
class SayteamHandler(object):
    message_type = 'N_SAYTEAM'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.handle_player_event('team_chat', player, message['text'])
