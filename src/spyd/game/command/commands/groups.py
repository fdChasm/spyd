from spyd.game.command.command_base import CommandBase
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.game.server_message_formatter import smf, info


@register("command")
class GroupsCommand(CommandBase):
    name = "groups"
    functionality = Functionality("spyd.game.commands.groups.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "(cn)"
    description = "Displays the groups of the indicated player or yourself."

    @classmethod
    def execute(cls, spyd_server, room, client, command_string, arguments, raw_args):
        if len(arguments):
            target = room.get_client(int(arguments[0]))
        else:
            target = client
            
        formatted_groups = ", ".join(map(lambda group: smf.format("{value#group}", group=group), target._client_permissions.get_group_names()))

        client.send_server_message(info("groups: {formatted_groups}", formatted_groups=formatted_groups))
