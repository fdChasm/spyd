from spyd.registry_manager import register
from spyd.game.edit.selection import Selection


@register('client_message_handler')
class EdittHandler(object):
    message_type = 'N_EDITT'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        texture = message['texture']
        all_faces = message['all_faces']
        room.handle_player_event('edit_texture', player, selection, texture, all_faces)
