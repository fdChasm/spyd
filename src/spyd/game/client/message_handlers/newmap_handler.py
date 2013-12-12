from spyd.registry_manager import register


@register('client_message_handler')
class NewmapHandler(object):
    message_type = 'N_NEWMAP'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('edit_new_map', client, message['size'])
