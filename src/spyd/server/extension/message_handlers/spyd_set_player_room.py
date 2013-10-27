from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.game.player.player import Player


@register('gep_message_handler')
class SpydSetPlayerRoomMessageHandler(object):
    msgtype = 'gep.set_player_room'
    execute = Functionality(msgtype)

    @classmethod
    def handle_message(cls, spyd_server, gep_client, message):
        room_name = message['room']
        player_uuid = message['player']
        player_message = message['message']

        player = Player.instances_by_uuid.get(player_uuid, None)

        if player is None:
            raise Exception("Unknown player.")

        client = player.client

        target_room = spyd_server.room_manager.get_room(name=room_name, fuzzy=False)

        if target_room is None:
            room_factory = spyd_server.room_manager.room_factory
            target_room = room_factory.build_room(room_name, 'temporary')
            target_room.temporary = True

        spyd_server.room_manager.client_change_room(client, target_room, False)

        if player_message:
            client.send_server_message(str(player_message))
