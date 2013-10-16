import unittest

from twisted.internet import task

from spyd.game.timing.game_clock import GameClock
from spyd.game.timing.resume_countdown import ResumeCountdown
from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
import spyd.game.room.room
from testing_utils.create_mock_player import create_mock_player
from testing_utils.dust2_meta_data import dust2_meta_data
from testing_utils.protocol.mock_server_write_helper import mock_server_write_helper


class TestRoomInstactf(unittest.TestCase):
    def setUp(self):
        self.clock = task.Clock()
        GameClock.clock = self.clock
        ScheduledCallbackWrapper.clock = self.clock
        ResumeCountdown.clock = self.clock
        
    def test_map_change_before_player_join_sends_correct_map_mode(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            room.change_map_mode('dust2', 'instactf')
            
            player_test_context.enter_room(room)
            
            player_test_context.assertHasReceivedMessageOfType('N_MAPCHANGE')
            
            map_change_message = player_test_context.get_received_messages_of_type('N_MAPCHANGE')[0]
            self.assertDictEqual(map_change_message, {'map_name': 'dust2', 'hasitems': False, 'mode_num': 12})
        
    def test_ictf_spawn_delay(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))
            player = player_test_context.player

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            room.change_map_mode('dust2', 'instactf')
            
            player_test_context.enter_room(room)
            
            player_test_context.clear_received_messages()
            
            room.on_player_suicide(player)
            
            room.on_player_request_spawn(player)
            
            player_test_context.assertHasNotReceivedMessageOfType('N_SPAWNSTATE')
            
            self.clock.advance(5)
            
            room.on_player_request_spawn(player)
            
            player_test_context.assertHasReceivedMessageOfType('N_SPAWNSTATE')
            
    def test_score_flag(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))
            player = player_test_context.player

            room = spyd.game.room.room.Room(map_meta_data_accessor={'dust2': dust2_meta_data})
            room.change_map_mode('dust2', 'instactf')
            
            player_test_context.enter_room(room)
            
            room.on_player_take_flag(player, 1, 0)
            player_test_context.assertHasReceivedMessageOfType('N_TAKEFLAG')
            room.on_player_take_flag(player, 0, 0)
            player_test_context.assertHasReceivedMessageOfType('N_SCOREFLAG')
            
    def test_suicide_drops_flag(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))
            player = player_test_context.player

            room = spyd.game.room.room.Room(map_meta_data_accessor={'dust2': dust2_meta_data})
            room.change_map_mode('dust2', 'instactf')
            
            player_test_context.enter_room(room)
            
            room.on_player_take_flag(player, 1, 0)
            room.on_player_suicide(player)
            player_test_context.assertHasReceivedMessageOfType('N_DROPFLAG')
            self.clock.advance(10)
            player_test_context.assertHasReceivedMessageOfType('N_RESETFLAG')
            
    def test_try_drop_flag_drops_flag(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))
            player = player_test_context.player

            room = spyd.game.room.room.Room(map_meta_data_accessor={'dust2': dust2_meta_data})
            room.change_map_mode('dust2', 'instactf')
            
            player_test_context.enter_room(room)
            
            room.on_player_take_flag(player, 1, 0)
            room.on_player_try_drop_flag(player)
            player_test_context.assertHasReceivedMessageOfType('N_DROPFLAG')
            self.clock.advance(10)
            player_test_context.assertHasReceivedMessageOfType('N_RESETFLAG')
            
    def test_score_10_flags_ends_game(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))
            player = player_test_context.player

            room = spyd.game.room.room.Room(map_meta_data_accessor={'dust2': dust2_meta_data})
            room.change_map_mode('dust2', 'instactf')
            
            player_test_context.enter_room(room)
            
            player_test_context.clear_received_messages()
            
            for i in xrange(10):
                player_test_context.assertHasNotReceivedMessageOfType('N_TIMEUP')
                room.on_player_take_flag(player, 1, i*2)
                player_test_context.assertHasReceivedMessageOfType('N_TAKEFLAG')
                room.on_player_take_flag(player, 0, 0)
                player_test_context.assertHasReceivedMessageOfType('N_SCOREFLAG')
            
            player_test_context.assertHasReceivedMessageOfType('N_TIMEUP')
            timeup_messages = player_test_context.get_received_messages_of_type('N_TIMEUP')
            self.assertAlmostEqual(timeup_messages[0]['timeleft'], 0.0)
