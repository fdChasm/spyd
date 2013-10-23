from spyd.game.command.command_base import CommandBase
from spyd.game.server_message_formatter import smf
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register

def format_cmd(command):
    return smf.format("{action#command.name}", command=command)

@register("command")
class RoomCommand(CommandBase):
    name = "commands"
    functionality = Functionality("spyd.game.commands.room.execute", "You do not have permission to execute {action#command}", command=name)
    usage = ""
    description = "Displays the list of commands you are permitted to execute."

    @classmethod
    def execute(cls, room, client, command_string, arguments, raw_args):
        available_commands = room.command_executer.get_available_commands(client)

        formatted_command_list = map(format_cmd, available_commands)

        client.send_server_message("\f7Commands: " + " | ".join(formatted_command_list))
