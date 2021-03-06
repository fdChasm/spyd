from spyd.game.command.command_base import CommandBase
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


@register("command")
class ResumeCommand(CommandBase):
    name = "resume"
    functionality = Functionality("spyd.game.commands.resume.execute", "You do not have permission to execute {action#command}", command=name)
    usage = ""
    description = "Resume the game."

    @classmethod
    def execute(cls, spyd_server, room, client, command_string, arguments, raw_args):
        room.handle_client_event('pause_game', client, 0)
