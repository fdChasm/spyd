from spyd.registry_manager import register
from spyd.game.edit.selection import Selection


@register('client_message_handler')
class RotateHandler(object):
    message_type = 'N_ROTATE'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        axis = message['axis']
        room.handle_player_event('edit_rotate', player, selection, axis)
