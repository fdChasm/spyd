from spyd.registry_manager import register


@register('client_message_handler')
class ItemlistHandler(object):
    message_type = 'N_ITEMLIST'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('item_list', client, message['items'])
