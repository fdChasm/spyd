from spyd.registry_manager import register
from spyd.game.edit.selection import Selection


@register('client_message_handler')
class EditfHandler(object):
    message_type = 'N_EDITF'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        direction = message['direction']
        mode = message['mode']
        room.handle_player_event('edit_face', player, selection, direction, mode)
