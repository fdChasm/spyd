from spyd.game.registry_manager import register
from spyd.permissions.functionality import Functionality
from spyd.game.client.client_message_handling_base import GenericError
from spyd.game.command.command_base import CommandBase
from spyd.game.room.exceptions import RoomEntryFailure

@register("command")
class RoomCommand(CommandBase):
    name = "room"
    functionality = Functionality("spyd.game.commands.room.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "<room name>"
    description = "Join a specified room."

    @classmethod
    def execute(cls, room, client, command_string, arguments):
        room_name = arguments[0]
        
        target_room = room.manager.get_room(room_name, True)
        
        if target_room is None:
            raise GenericError("Could not resolve {value#room_name} to a room.", room_name=room_name)
        
        room.manager.client_change_room(client, target_room)
