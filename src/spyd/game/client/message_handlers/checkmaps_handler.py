from spyd.registry_manager import register


@register('client_message_handler')
class CheckmapsHandler(object):
    message_type = 'N_CHECKMAPS'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('check_maps', client)
