from spyd.registry_manager import register


@register('client_message_handler')
class AuthtryHandler(object):
    message_type = 'N_AUTHTRY'

    @staticmethod
    def handle(client, room, message):
        authdomain = message['authdomain']
        authname = message['authname']

        deferred = client.auth(authdomain, authname)  # @UnusedVariable
