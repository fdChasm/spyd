from spyd.registry_manager import register


@register('room_client_event_handler')
class FlagListHandler(object):
    event_type = 'flag_list'

    @staticmethod
    def handle(room, client, flag_list):
        room.gamemode.on_client_flag_list(client, flag_list)
