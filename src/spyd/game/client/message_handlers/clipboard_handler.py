from spyd.registry_manager import register


@register('client_message_handler')
class ClipboardHandler(object):
    message_type = 'N_CLIPBOARD'

    @staticmethod
    def handle(client, room, message):
        pass
