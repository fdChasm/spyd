from spyd.registry_manager import register


@register('client_message_handler')
class ClearbansHandler(object):
    message_type = 'N_CLEARBANS'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('clear_bans', client)
