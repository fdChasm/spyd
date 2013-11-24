from spyd.game.command.command_base import CommandBase
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.game.server_message_formatter import info
from spyd.game.client.exceptions import UsageError


@register("command")
class ResumeDelayCommand(CommandBase):
    name = "resumedelay"
    functionality = Functionality("spyd.game.commands.resumedelay.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "(seconds)"
    description = "View or set the amount of time to count down before starting or resuming a game."

    @classmethod
    def execute(cls, room, client, command_string, arguments, raw_args):
        if len(arguments):
            try:
                room.resume_delay = max(0, min(10, int(arguments[0])))
                room._broadcaster.server_message(info("{name#client} has set the resume delay to {value#resume_delay} seconds.", client=client, resume_delay=room.resume_delay))
            except:
                raise UsageError("The resume delay must be an number.")
        else:
            client.send_server_message(info("The resume delay is {value#resume_delay} seconds.", resume_delay=room.resume_delay))
