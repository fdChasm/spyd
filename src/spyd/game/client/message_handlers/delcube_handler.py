from spyd.registry_manager import register
from spyd.game.edit.selection import Selection


@register('client_message_handler')
class DelcubeHandler(object):
    message_type = 'N_DELCUBE'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        room.handle_player_event('edit_delete_cubes', player, selection)
