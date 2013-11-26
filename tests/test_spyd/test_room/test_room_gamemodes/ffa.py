import unittest

from twisted.internet import task

from cube2common.constants import item_types
from spyd.game.map.item import Item
import spyd.game.room.room
from spyd.game.timing.game_clock import GameClock
from spyd.game.timing.resume_countdown import ResumeCountdown
from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from testing_utils.complex_meta_data import complex_meta_data
from testing_utils.create_mock_player import create_mock_player
from testing_utils.protocol.mock_server_write_helper import mock_server_write_helper


def itemTypeSpawnCount(player_test_context, item_type_id):
    count = 0
    item_spawn_messages = player_test_context.get_received_messages_of_type('N_ITEMSPAWN')
    for item_spawn_message in item_spawn_messages:
        if item_spawn_message['item'].type == item_type_id:
            count += 1
    return count

def isItemIndexSpawned(player_test_context, item_index):
    all_messages = player_test_context.get_all_received_messages()
    
    spawned = False
    for message_type, message in all_messages:
        if message_type == "N_ITEMLIST":
            spawned = message['items'][item_index].spawned
        elif message_type == "N_ITEMSPAWN":
            if message['item'].index == item_index:
                spawned = True
        elif message_type == "N_ITEMACC":
            if message['item'].index == item_index:
                spawned = False
    return spawned

def listUsedItemIndexes(player_test_context):
    item_list_message = player_test_context.get_received_messages_of_type('N_ITEMLIST')[0]

    item_list = item_list_message['items']

    for index in xrange(len(item_list)):
        item = item_list[index]
        if isinstance(item, Item):
            print index, item

class TestRoomFFA(unittest.TestCase):
    def setUp(self):
        self.clock = task.Clock()
        GameClock.clock = self.clock
        ScheduledCallbackWrapper.clock = self.clock
        ResumeCountdown.clock = self.clock

    def test_map_change_before_player_join_sends_correct_map_mode(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={'complex': complex_meta_data})
            room.change_map_mode('complex', 'ffa')

            player_test_context.enter_room(room)

            player_test_context.assertHasReceivedMessageOfType('N_MAPCHANGE')

            map_change_message = player_test_context.get_received_messages_of_type('N_MAPCHANGE')[0]
            self.assertDictEqual(map_change_message, {'map_name': 'complex', 'hasitems': False, 'mode_num': 0})

    def test_sends_item_list(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={'complex': complex_meta_data})
            room.change_map_mode('complex', 'ffa')

            player_test_context.enter_room(room)

            player_test_context.assertHasReceivedMessageOfType('N_ITEMLIST')

    def test_sends_yellow_and_green_armour_spawns_after_20(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={'complex': complex_meta_data})
            room.change_map_mode('complex', 'ffa')

            player_test_context.enter_room(room)

            self.clock.advance(19.9)

            self.assertEqual(itemTypeSpawnCount(player_test_context, item_types.I_GREENARMOUR), 0)
            self.assertEqual(itemTypeSpawnCount(player_test_context, item_types.I_YELLOWARMOUR), 0)

            self.clock.advance(0.1)

            self.assertEqual(itemTypeSpawnCount(player_test_context, item_types.I_GREENARMOUR), 1)
            self.assertEqual(itemTypeSpawnCount(player_test_context, item_types.I_YELLOWARMOUR), 1)

    def test_take_item_sends_ack(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={'complex': complex_meta_data})
            room.change_map_mode('complex', 'ffa')

            player_test_context.enter_room(room)

            room.handle_player_event('pickup_item', player_test_context.player, item_index=79)

            player_test_context.assertHasReceivedMessageOfType('N_ITEMACC')

    def test_take_bullets_respawn_in_16_with_1_player(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={'complex': complex_meta_data})
            room.change_map_mode('complex', 'ffa')

            player_test_context.enter_room(room)

            room.handle_player_event('pickup_item', player_test_context.player, item_index=79)

            self.clock.advance(15.9)

            self.assertFalse(isItemIndexSpawned(player_test_context, item_index=79))

            self.clock.advance(0.1)
            
            self.assertTrue(isItemIndexSpawned(player_test_context, item_index=79))
            
    def test_take_bullets_then_second_player_joins(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player_test_context2 = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={'complex': complex_meta_data})
            room.change_map_mode('complex', 'ffa')

            player_test_context1.enter_room(room)

            room.handle_player_event('pickup_item', player_test_context1.player, item_index=79)

            player_test_context2.enter_room(room)
            
            self.clock.advance(15.9)
            
            self.assertFalse(isItemIndexSpawned(player_test_context2, item_index=79))

    def test_immediate_map_change_cancels_itemspawns(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={'complex': complex_meta_data})
            room.change_map_mode('complex', 'ffa')

            self.clock.advance(2)

            player_test_context.enter_room(room)

            self.clock.advance(2)

            room.change_map_mode('complex', 'insta')

            player_test_context.clear_received_messages()

            self.clock.advance(30)

            player_test_context.assertHasNotReceivedMessageOfType('N_ITEMSPAWN')
