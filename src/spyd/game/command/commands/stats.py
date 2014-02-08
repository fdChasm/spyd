from spyd.game.command.command_base import CommandBase
from spyd.game.server_message_formatter import info
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.utils.prettytime import shortDurationString

"\fs\f1Name:\f7 %s  \f1Frags:\f7 %d  \f1Deaths:\f7 %d  \f1Suicides:\f7 %d  \f1Teamkills:\f7 %d  \f1Accuracy:\f7 %d%%  \f1Online:\f7 %s\fr"

stats_msg = "Name: {name#player}, Frags: {value#player.state.frags}, Deaths: {value#player.state.deaths}, Suicides: {value#player.state.suicides}, Teamkills: {value#player.state.teamkills}, Accuracy: {value#player.state.acc_formatted}, Online: {value#time_online_str}"

@register("command")
class RoomCommand(CommandBase):
    name = "stats"
    functionality = Functionality("spyd.game.commands.stats.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "(cn)"
    description = "Displays the stats of the indicated player or yourself."

    @classmethod
    def execute(cls, room, client, command_string, arguments, raw_args):
        if len(arguments):
            player = room.get_player(int(arguments[0]))
        else:
            player = client.get_player()

        time_online_str = shortDurationString(player.client.time_online)
        client.send_server_message(info(stats_msg, player=player, time_online_str=time_online_str))
