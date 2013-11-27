from spyd.registry_manager import register


@register('room_client_event_handler')
class CommandHandler(object):
    event_type = 'command'

    @staticmethod
    def handle(room, client, command):
        pass
