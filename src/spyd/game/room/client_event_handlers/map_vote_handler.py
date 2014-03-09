from twisted.internet import defer

from spyd.game.client.exceptions import InsufficientPermissions
from spyd.game.gamemode import get_mode_name_from_num
from spyd.game.map.resolve_map_name import resolve_map_name
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


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

        map_name = yield resolve_map_name(room, map_name)

        room.change_map_mode(map_name, mode_name)
