from spyd.registry_manager import register


@register('client_message_handler')
class MapcrcHandler(object):
    message_type = 'N_MAPCRC'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('map_crc', client, message['mapcrc'])
