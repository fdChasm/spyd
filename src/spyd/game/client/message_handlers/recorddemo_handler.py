from spyd.registry_manager import register


@register('client_message_handler')
class RecorddemoHandler(object):
    message_type = 'N_RECORDDEMO'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('set_demo_recording', client, message['value'])
