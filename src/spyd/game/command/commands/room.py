from spyd.game.registry_manager import register
from spyd.permissions.functionality import Functionality

@register("command")
class RoomCommand(object):
    command = "room"
    functionality = Functionality("spyd.game.commands.room.execute")
    usage = "<room name>"
    description = "Join a specified room."

    @staticmethod
    def execute(room, client, argument_string):
        pass