from spyd.registry_manager import register
from spyd.permissions.functionality import Functionality
import time

@register('gep_message_handler')
class SpydPingMessageHandler(object):
    msgtype = 'gep.ping'
    execute = Functionality(msgtype)

    @classmethod
    def handle_message(cls, spyd_server, gep_client, message):
        server_time = int(time.time() * 1000000)
        client_time = message['time']
        gep_client.send({'msgtype': 'gep.pong', 'client_time': client_time, 'server_time': server_time}, message.get('reqid'))
