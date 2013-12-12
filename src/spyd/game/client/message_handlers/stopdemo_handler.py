from spyd.registry_manager import register


@register('client_message_handler')
class StopdemoHandler(object):
    message_type = 'N_STOPDEMO'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('stop_demo_recording', client)
