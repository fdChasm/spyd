from twisted.internet import defer

from spyd.game.client.exceptions import InsufficientPermissions, GenericError
from spyd.game.gamemode import get_mode_name_from_num
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.utils.match_fuzzy import match_fuzzy


set_map_mode_functionality = Functionality("spyd.game.room.set_map_mode", 'Insufficient permissions to force a map/mode change.')

@register('room_client_event_handler')
class MapVoteHandler(object):
    event_type = 'map_vote'

    @staticmethod
    @defer.inlineCallbacks
    def handle(room, client, map_name, mode_num):
        if not client.allowed(set_map_mode_functionality):
            raise InsufficientPermissions(set_map_mode_functionality.denied_message)

        mode_name = get_mode_name_from_num(mode_num)

        valid_map_names = yield room._map_mode_state.get_map_names()

        map_name_match = match_fuzzy(map_name, valid_map_names)

        if map_name_match is None:
            raise GenericError('Could not resolve map name to valid map. Please try again.')

        room.change_map_mode(map_name_match, mode_name)
