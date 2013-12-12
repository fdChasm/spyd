from spyd.registry_manager import register


@register('client_message_handler')
class GetmapHandler(object):
    message_type = 'N_GETMAP'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('edit_get_map', client)
