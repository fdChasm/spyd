from spyd.game.command.command_base import CommandBase
from spyd.game.server_message_formatter import info
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


room_info_msg = "Room: {room#room.name}, Players: {value#room.player_count}, Mode: {mode#room.mode_name}, Map: {map#room.map_name}"

@register("command")
class RoomCommand(CommandBase):
    name = "rooms"
    functionality = Functionality("spyd.game.commands.room.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "<room name>"
    description = "Displays the rooms on the server, their player counts, modes, and maps."

    @classmethod
    def execute(cls, room, client, command_string, arguments):
        for room in room.manager.rooms.itervalues():
            if room.empty: continue
            client.send_server_message(info(room_info_msg, room=room))
