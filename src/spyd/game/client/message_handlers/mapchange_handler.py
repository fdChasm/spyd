from spyd.registry_manager import register


@register('client_message_handler')
class MapchangeHandler(object):
    message_type = 'N_MAPCHANGE'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('map_vote', client, message['map_name'], message['mode_num'])
