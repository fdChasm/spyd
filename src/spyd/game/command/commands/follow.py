from spyd.registry_manager import register
from spyd.permissions.functionality import Functionality
from spyd.game.client.client_message_handling_base import GenericError
from spyd.game.command.command_base import CommandBase

@register("command")
class RoomCommand(CommandBase):
    name = "follow"
    functionality = Functionality("spyd.game.commands.room.execute", "You do not have permission to execute {action#command}", command=name)
    usage = ""
    description = "Follow the last player to leave this room."

    @classmethod
    def execute(cls, room, client, command_string, arguments):
        room_name = room.last_destination_room
        
        if room_name is None:
            raise GenericError("No players have left this room for another recently. Perhaps join another existing room with {action#room}.", room='room')
        
        target_room = room.manager.get_room(room_name, True)
        
        if target_room is None:
            raise GenericError("Could not join {value#room_name}. Room no longer exists. Perhaps create it with {action#room_create}", room_name=room_name, room_create='room_create')
        
        room.manager.client_change_room(client, target_room)
