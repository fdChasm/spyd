from spyd.registry_manager import register


@register('client_message_handler')
class KickHandler(object):
    message_type = 'N_KICK'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('kick', client, message['target_cn'], message['reason'])
