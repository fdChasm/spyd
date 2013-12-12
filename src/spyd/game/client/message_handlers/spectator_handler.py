from spyd.registry_manager import register


@register('client_message_handler')
class SpectatorHandler(object):
    message_type = 'N_SPECTATOR'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('set_spectator', client, message['target_cn'], bool(message['value']))
