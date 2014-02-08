from spyd.game.client.exceptions import InsufficientPermissions, GenericError
from spyd.game.command.command_base import CommandBase
from spyd.game.gamemode import gamemodes
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.utils.match_fuzzy import match_fuzzy
from spyd.game.room.client_event_handlers.map_vote_handler import set_map_mode_functionality


@register("command")
class ChangeMapCommand(CommandBase):
    name = "<mode>"
    functionality = Functionality("spyd.game.commands.resume.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "<map>"
    description = "Change the mode and map."

    @classmethod
    def handles(cls, room, client, command_string):
        return command_string in gamemodes

    @classmethod
    def execute(cls, spyd_server, room, client, command_string, arguments, raw_args):
        if not client.allowed(set_map_mode_functionality):
            raise InsufficientPermissions(set_map_mode_functionality.denied_message)

        mode_name = command_string
        map_name = arguments[0]

        valid_map_names = room._map_mode_state.get_map_names()
        map_name_match = match_fuzzy(map_name, valid_map_names)

        if map_name_match is None:
            raise GenericError('Could not resolve map name to valid map. Please try again.')

        room.change_map_mode(map_name_match, mode_name)
