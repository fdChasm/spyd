from spyd.protocol import swh
from spyd.registry_manager import register


@register('client_message_handler')
class PingHandler(object):
    message_type = 'N_PING'

    @staticmethod
    def handle(client, room, message):
        with client.sendbuffer(1, False) as cds:
            swh.put_pong(cds, message['cmillis'])
