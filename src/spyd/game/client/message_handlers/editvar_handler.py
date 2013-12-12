from spyd.registry_manager import register


@register('client_message_handler')
class EditvarHandler(object):
    message_type = 'N_EDITVAR'

    @staticmethod
    def handle(client, room, message):
        pass
