from spyd.registry_manager import register


@register('client_message_handler')
class InitflagsHandler(object):
    message_type = 'N_INITFLAGS'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('flag_list', client, message['flags'])
