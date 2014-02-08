from spyd.game.command.command_base import CommandBase
from spyd.game.server_message_formatter import info
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register

@register("command")
class InfoCommand(CommandBase):
    name = "info"
    functionality = Functionality("spyd.game.commands.info.execute", "You do not have permission to execute {action#command}", command=name)
    usage = ""
    description = "Displays the server info message."

    @classmethod
    def execute(cls, spyd_server, room, client, command_string, arguments, raw_args):
        client.send_server_message(info(spyd_server.server_info_model.value))
