from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
import traceback


@register('gep_message_handler')
class SpydSetRoomPausedMessageHandler(object):
    msgtype = 'set_room_paused'
    execute = Functionality(msgtype)

    @classmethod
    def handle_message(cls, spyd_server, gep_client, message):
        room_name = message['room']
        pause = message['pause']
        room_message = message['message']

        target_room = spyd_server.room_manager.get_room(name=room_name, fuzzy=False)

        if target_room is None:
            raise Exception("Unknown room.")
        try:
            if pause:
                target_room.pause()
            else:
                target_room.resume()

            if room_message:
                target_room.server_message(str(room_message))
        except:
            traceback.print_exc()

        gep_client.send({"msgtype": "status", "status": "success"}, message.get('reqid'))
