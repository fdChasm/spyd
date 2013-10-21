from spyd.game.client.client_message_handling_base import InsufficientPermissions, GenericError
from spyd.game.command.command_base import CommandBase
from spyd.game.server_message_formatter import info
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.utils import timestring, prettytime


MAXTIMELEFT = 60 * 60 * 24 * 30

timeleft_set_str = "{name#client} has set the remaining time to {value#timeleft}."
timeleft_get_str = "Remaining time {value#timeleft}."

set_temporary_room_timeleft = Functionality("spyd.game.commands.timeleft.set_temporary_room", "You do not have permission to set the time in temporary rooms.")
set_permanent_room_timeleft = Functionality("spyd.game.commands.timeleft.set_permanent_room", "You do not have permission to set the time in permanent rooms.")

@register("command")
class TimeleftCommand(CommandBase):
    name = "timeleft"
    functionality = Functionality("spyd.game.commands.timeleft.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "(time string)"
    description = "View or set the amount of time left in the match. Valid time strings could be; +2m -30s 10m 2y"

    @classmethod
    def execute(cls, room, client, command_string, arguments, raw_args):
        if len(arguments):
            if room.temporary:
                if not client.allowed(set_temporary_room_timeleft):
                    raise InsufficientPermissions(set_temporary_room_timeleft.denied_message)
            else:
                if not client.allowed(set_permanent_room_timeleft):
                    raise InsufficientPermissions(set_permanent_room_timeleft.denied_message)

            try:
                modifier, value = timestring.parseTimeString(raw_args)

                if modifier == '+':
                    new_timeleft = min(MAXTIMELEFT, max(0, room.timeleft + value))
                elif modifier == '-':
                    new_timeleft = min(MAXTIMELEFT, max(0, room.timeleft - value))
                elif modifier == '=':
                    new_timeleft = min(MAXTIMELEFT, max(0, value))

                timeleft = prettytime.createDurationString(new_timeleft)
                room._broadcaster.server_message(info(timeleft_set_str, client=client, timeleft=timeleft))

                room.timeleft = new_timeleft

            except timestring.MalformedTimeString:
                raise GenericError("Invalid time string specified.")
        else:
            timeleft = prettytime.createDurationString(room.timeleft)
            client.send_server_message(info(timeleft_get_str, timeleft=timeleft))
