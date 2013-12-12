from spyd.registry_manager import register


@register('client_message_handler')
class MastermodeHandler(object):
    message_type = 'N_MASTERMODE'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('set_master_mode', client, message['mastermode'])
