from spyd.registry_manager import register


@register('client_message_handler')
class ForceintermissionHandler(object):
    message_type = 'N_FORCEINTERMISSION'

    @staticmethod
    def handle(client, room, message):
        pass
