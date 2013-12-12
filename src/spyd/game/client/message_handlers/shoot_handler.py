from cube2common.vec import vec
from spyd.registry_manager import register
from spyd.utils.dictionary_get import dictget


@register('client_message_handler')
class ShootHandler(object):
    message_type = 'N_SHOOT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        shot_id = message['shot_id']
        gun = message['gun']
        from_pos = vec(*dictget(message, 'fx', 'fy', 'fz'))
        to_pos = vec(*dictget(message, 'tx', 'ty', 'tz'))
        hits = message['hits']
        room.handle_player_event('shoot', player, shot_id, gun, from_pos, to_pos, hits)
