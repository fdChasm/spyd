from spyd.registry_manager import register

@register('room_client_event_handler')
class ItemListHandler(object):
    event_type = 'item_list'

    @staticmethod
    def handle(room, client, item_list):
        room.gamemode.on_client_item_list(client, item_list)

