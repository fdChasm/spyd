from spyd.registry_manager import register
from spyd.game.edit.selection import Selection


@register('client_message_handler')
class EditmHandler(object):
    message_type = 'N_EDITM'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        material = message['material']
        material_filter = message['material_filter']
        room.handle_player_event('edit_material', player, selection, material, material_filter)
