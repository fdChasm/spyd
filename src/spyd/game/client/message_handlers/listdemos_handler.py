from spyd.registry_manager import register


@register('client_message_handler')
class ListdemosHandler(object):
    message_type = 'N_LISTDEMOS'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('list_demos', client)
