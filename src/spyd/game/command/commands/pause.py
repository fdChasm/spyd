from spyd.game.command.command_base import CommandBase
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


@register("command")
class PauseCommand(CommandBase):
    name = "pause"
    functionality = Functionality("spyd.game.commands.pause.execute", "You do not have permission to execute {action#command}", command=name)
    usage = ""
    description = "Pause the game."

    @classmethod
    def execute(cls, room, client, command_string, arguments, raw_args):
        room.on_client_pause_game(client, pause=1)
