from spyd.registry_manager import register
from spyd.utils.dictionary_get import dictget


@register('client_message_handler')
class EditentHandler(object):
    message_type = 'N_EDITENT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        entity_id = message['entid']
        entity_type = message['type']
        x, y, z = dictget(message, 'x', 'y', 'z')
        attrs = message['attrs']
        room.handle_player_event('edit_entity', player, entity_id, entity_type, x, y, z, attrs)
