import unittest
from spyd.game.room.room_manager import RoomManager
from mock import Mock


class TestRoomManager(unittest.TestCase):
    def setUp(self):
        self.room = Mock()
        self.room.name = "test"
        self.room_manager = RoomManager()

    def test_set_factory(self):
        room_factory = Mock()
        self.room_manager.set_factory(room_factory)
        self.assertEqual(self.room_manager.room_factory, room_factory)
    
    def test_add_room(self):
        self.room_manager.add_room(self.room)
        self.assertEqual(self.room_manager.rooms.get('test', None), self.room)

    def test_get_room_no_fuzzy_failure(self):
        self.assertEqual(self.room_manager.get_room('test', False), None)

    def test_get_room_no_fuzzy_success(self):
        self.room_manager.add_room(self.room)
        self.assertEqual(self.room_manager.get_room('test', False), self.room)

    def test_get_room_with_fuzzy_failure(self):
        self.assertEqual(self.room_manager.get_room('test', True), None)

    def test_get_room_with_fuzzy_success(self):
        self.room_manager.add_room(self.room)
        self.assertEqual(self.room_manager.get_room('tesz', True), self.room)

    def test_on_room_player_count_changed(self):
        room = self.room

        conditions = [
            {'empty': True, 'temporary': True, 'rooms': {}},
            {'empty': False, 'temporary': True, 'rooms': {'test': room}},
            {'empty': True, 'temporary': False, 'rooms': {'test': room}},
            {'empty': False, 'temporary': False, 'rooms': {'test': room}},
        ]
        for condition in conditions:
            room_manager = RoomManager()

            room.empty = condition['empty']
            room.temporary = condition['temporary']

            room_manager.add_room(room)

            room_manager.on_room_player_count_changed(room)

            self.assertEqual(room_manager.rooms, condition['rooms'])

    def test_find_room_for_client_ip_failure(self):
        self.room.contains_client_with_ip = Mock(return_value=False)
        self.room_manager.add_room(self.room)
        self.assertEqual(self.room_manager.find_room_for_client_ip('127.0.0.1'), None)

    def test_find_room_for_client_ip_success(self):
        self.room.contains_client_with_ip = Mock(return_value=True)
        self.room_manager.add_room(self.room)
        self.assertEqual(self.room_manager.find_room_for_client_ip('127.0.0.1'), self.room)
