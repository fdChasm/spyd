from mock import Mock
from twisted.internet import defer

from spyd.game.room.room import Room


def mock_room(map_names=(u'complex',)):
    room = Mock(spec=Room)
    room.manager = Mock()
    room.get_map_names = Mock(return_value=defer.succeed(map_names))
    return room
