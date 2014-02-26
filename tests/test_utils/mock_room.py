from mock import Mock
from spyd.game.room.room import Room


def mock_room(map_names=(u'complex')):
    room = Mock(spec=Room)
    room.manager = Mock()
    room.get_map_names = Mock(return_value=map_names)
    return room
