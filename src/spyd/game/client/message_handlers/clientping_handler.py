from spyd.protocol import swh
from spyd.registry_manager import register


@register('client_message_handler')
class ClientpingHandler(object):
    message_type = 'N_CLIENTPING'

    @staticmethod
    def handle(client, room, message):
        ping = message['ping']
        client.ping_buffer.add(ping)
        player = client.get_player()
        swh.put_clientping(player.state.messages, ping)
