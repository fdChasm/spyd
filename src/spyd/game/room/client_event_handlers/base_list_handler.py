from spyd.registry_manager import register

@register('room_client_event_handler')
class BaseListHandler(object):
    event_type = 'base_list'

    @staticmethod
    def handle(room, client, base_list):
        room.gamemode.on_client_base_list(client, base_list)

