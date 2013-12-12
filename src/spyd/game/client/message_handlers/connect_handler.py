from spyd.registry_manager import register


@register('client_message_handler')
class ConnectHandler(object):
    message_type = 'N_CONNECT'

    @staticmethod
    def handle(client, room, message):
        if not client.is_connected:
            client.connect_received(message)
