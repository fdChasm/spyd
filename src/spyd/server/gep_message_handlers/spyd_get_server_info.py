from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


@register('gep_message_handler')
class SpydGetServerInfoMessageHandler(object):
    msgtype = 'get_server_info'
    execute = Functionality(msgtype)

    @classmethod
    def handle_message(cls, spyd_server, gep_client, message):
        room_manager = spyd_server.room_manager

        server_info = {
            "rooms": room_manager.rooms.keys()
        }

        gep_client.send({'msgtype': 'server_info', 'server_info': server_info}, message.get('reqid'))
