from spyd.registry_manager import register


@register('client_message_handler')
class ExplodeHandler(object):
    message_type = 'N_EXPLODE'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        cmillis = message['cmillis']
        gun = message['gun']
        explode_id = message['explode_id']
        hits = message['hits']
        room.handle_player_event('explode', player, cmillis, gun, explode_id, hits)
