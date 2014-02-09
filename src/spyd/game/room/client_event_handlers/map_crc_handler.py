from spyd.registry_manager import register

@register('room_client_event_handler')
class MapCrcHandler(object):
    event_type = 'map_crc'

    @staticmethod
    def handle(room, client, crc):
        # TODO: Implement optional spectating of clients without valid map CRC's
        room.ready_up_controller.on_crc(client, crc)

