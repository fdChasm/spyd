from spyd.registry_manager import register
from spyd.game.edit.selection import Selection


@register('client_message_handler')
class ReplaceHandler(object):
    message_type = 'N_REPLACE'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        texture = message['texture']
        new_texture = message['new_texture']
        in_selection = message['in_selection']
        room.handle_player_event('edit_replace', player, selection, texture, new_texture, in_selection)
