from spyd.registry_manager import register


@register('client_message_handler')
class TakeflagHandler(object):
    message_type = 'N_TAKEFLAG'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('take_flag', player, message['flag'], message['version'])
