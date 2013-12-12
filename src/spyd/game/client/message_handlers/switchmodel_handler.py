from spyd.registry_manager import register


@register('client_message_handler')
class SwitchmodelHandler(object):
    message_type = 'N_SWITCHMODEL'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('switch_model', player, message['playermodel'])
