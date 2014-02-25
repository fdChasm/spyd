from mock import Mock
from spyd.game.room.room import Room


def mock_room():
    room = Mock(spec=Room)
    room.manager = Mock()
    return room
