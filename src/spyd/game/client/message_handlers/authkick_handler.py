from spyd.registry_manager import register


@register('client_message_handler')
class AuthkickHandler(object):
    message_type = 'N_AUTHKICK'

    @staticmethod
    def handle(client, room, message):
        authdomain = message['authdomain']
        authname = message['authname']
        target_pn = message['target_cn']
        reason = message['reason']

        deferred = client.auth(authdomain, authname)
        callback = lambda r: room.handle_client_event('kick', client, target_pn, reason)
        deferred.addCallbacks(callback, callback)
