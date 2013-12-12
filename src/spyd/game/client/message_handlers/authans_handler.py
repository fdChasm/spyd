from spyd.registry_manager import register


@register('client_message_handler')
class AuthansHandler(object):
    message_type = 'N_AUTHANS'

    @staticmethod
    def handle(client, room, message):
        authdomain = message['authdomain']
        authid = message['authid']
        answer = message['answer']
        client.answer_auth_challenge(authdomain, authid, answer)
