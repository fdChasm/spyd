from spyd.registry_manager import register


@register('client_message_handler')
class SetmasterHandler(object):
    message_type = 'N_SETMASTER'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('set_master', client, message['target_cn'], message['pwdhash'], message['value'])
