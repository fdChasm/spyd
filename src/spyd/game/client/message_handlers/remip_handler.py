from spyd.registry_manager import register


@register('client_message_handler')
class RemipHandler(object):
    message_type = 'N_REMIP'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('edit_remip', client)
