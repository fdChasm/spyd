import re

from spyd.game.client.client_message_handling_base import GenericError
from spyd.game.command.command_base import CommandBase
from spyd.registry_manager import register
from spyd.permissions.functionality import Functionality
from spyd.utils.filtertext import filtertext
from cube2common.constants import MAXROOMLEN


duel_room_pattern = re.compile('^\d+x\d+$')

@register("command")
class RoomCreateCommand(CommandBase):
    name = "room_create"
    functionality = Functionality("spyd.game.commands.room_create.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "<room name>"
    description = "Create a room."

    @classmethod
    def execute(cls, room, client, command_string, arguments):
        room_name = filtertext(arguments[0], True, MAXROOMLEN)
        
        target_room = room.manager.get_room(room_name, False)
        
        if target_room is not None:
            raise GenericError("Room {room#room} already exists, use {action#command} to enter it.", room=target_room.name, command="room")

        if duel_room_pattern.match(room_name):
            raise GenericError("Room {room#room_name} cannot be created for you because room names with the pattern '#x#' are reserved for 1v1 games.", room_name=room_name)
        
        room_factory = room.manager.room_factory
        target_room = room_factory.build_room(room_name, 'temporary')
        
        target_room.masters.add(client)
        
        room.manager.client_change_room(client, target_room)
