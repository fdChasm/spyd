from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


@register('gep_message_handler')
class SpydGetPlayerInfoMessageHandler(object):
    msgtype = 'get_room_info'
    execute = Functionality(msgtype)

    @classmethod
    def handle_message(cls, spyd_server, gep_client, message):
        room_name = message['room']

        room = spyd_server.room_manager.get_room(name=room_name, fuzzy=False)

        if room is None:
            raise Exception("Unknown room.")

        room_info = {
            'is_paused': room.is_paused,
            'is_resuming': room.is_resuming,
            'timeleft': room.timeleft,
            'is_intermission': room.is_intermission,
            'resume_delay': room.resume_delay,
            'mode': room.mode_name,
            'map': room.map_name,
            'players': map(lambda player: player.uuid, room.players),
            'show_awards': room.show_awards,
            'mastermode': room.mastermode,
            'mastermask': room.mastermask,
            'temporary': room.temporary,
            'maxplayers': room.maxplayers
        }

        gep_client.send({'msgtype': 'room_info', 'room': room.name, 'room_info': room_info}, message.get('reqid'))
