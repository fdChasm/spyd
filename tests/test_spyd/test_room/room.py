import unittest

from twisted.internet import task

import spyd.game.room.room
from spyd.game.timing.game_clock import GameClock
from spyd.game.timing.resume_countdown import ResumeCountdown
from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from testing_utils.create_mock_player import create_mock_player
from testing_utils.protocol.mock_server_write_helper import mock_server_write_helper
from spyd.utils.value_model import ValueModel
from spyd.game.gamemode import gamemodes
from cube2common.constants import INTERMISSIONLEN
from twisted.internet.defer import setDebugging
from mock import MagicMock


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.clock = task.Clock()
        GameClock.clock = self.clock
        ScheduledCallbackWrapper.clock = self.clock
        ResumeCountdown.clock = self.clock
        
        setDebugging(True)

    def test_add_player_sends_mapchange(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            player_test_context.enter_room(room)
            
            player_test_context.assertHasReceivedMessageOfType('N_MAPCHANGE')
            
    def test_add_player_sends_timeup(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            room.change_map_mode('dust2', 'instactf')
            player_test_context.enter_room(room)
            
            player_test_context.assertHasReceivedMessageOfType('N_TIMEUP')
            
    def test_add_player_to_paused_room_sends_paused_true(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player_test_context2 = stack.enter_context(create_mock_player(self, 1))
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            player_test_context1.enter_room(room)
            room.pause()
            player_test_context2.enter_room(room)
            
            player_test_context2.assertHasReceivedMessageOfType('N_PAUSEGAME')

            messages = player_test_context2.get_received_messages_of_type('N_PAUSEGAME')
            self.assertTrue(messages[0]['paused'])
            
    def test_add_player_to_room_with_resumedelay_sends_paused_true(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            room.resume_delay = 5
            player_test_context.enter_room(room)
            
            player_test_context.assertHasReceivedMessageOfType('N_PAUSEGAME')

            messages = player_test_context.get_received_messages_of_type('N_PAUSEGAME')
            self.assertTrue(messages[0]['paused'])
            
    def test_add_player_to_room_with_resumedelay_resumes_after_delay(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            room.resume_delay = 5
            player_test_context.enter_room(room)
            player_test_context.clear_received_messages()
            self.clock.advance(room.resume_delay)
            
            player_test_context.assertHasReceivedMessageOfType('N_PAUSEGAME')

            messages = player_test_context.get_received_messages_of_type('N_PAUSEGAME')
            self.assertFalse(messages[0]['paused'])
            
    def test_resume_sends_resumed_message(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            player_test_context.enter_room(room)
            room.pause()
            player_test_context.clear_received_messages()
            room.resume()
            
            player_test_context.assertHasReceivedMessageOfType('N_PAUSEGAME')

            messages = player_test_context.get_received_messages_of_type('N_PAUSEGAME')
            self.assertFalse(messages[0]['paused'])
            
    def test_set_name_sends_servinfo(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))

            server_name_model = ValueModel("123456789ABCD")

            room = spyd.game.room.room.Room(server_name_model, map_meta_data_accessor={})
            player_test_context.enter_room(room)
            
            player_test_context.assertHasReceivedMessageOfType('N_SERVINFO')
            
            player_test_context.clear_received_messages()
            room.name = "hello"
            
            player_test_context.assertHasReceivedMessageOfType('N_SERVINFO')

            messages = player_test_context.get_received_messages_of_type('N_SERVINFO')
            self.assertEqual(messages[0]['description'], '123456789ABCD \x0c1hello\x0c7')
            
    def test_add_player_to_room_sends_init_client_to_others(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player_test_context2 = stack.enter_context(create_mock_player(self, 1))
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            player_test_context1.enter_room(room)
            player_test_context2.enter_room(room)
            
            player_test_context1.assertHasReceivedMessageOfType('N_INITCLIENT')
            
    def test_remove_player_from_room_sends_cdis_to_others(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player_test_context2 = stack.enter_context(create_mock_player(self, 1))
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={}, room_manager=MagicMock())
            
            player_test_context1.enter_room(room)
            player_test_context2.enter_room(room)
            
            player_test_context2.leave_room(room)
            
            player_test_context1.assertHasReceivedMessageOfType('N_CDIS')
            
    def test_remove_player_from_room_player_stops_receiving_messages(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={}, room_manager=MagicMock())
            player_test_context.enter_room(room)
            player_test_context.leave_room(room)
            player_test_context.clear_received_messages()
            room.pause()
            
            self.assertLessEqual(len(player_test_context.get_all_received_messages()), 0)
            
    def test_on_suicide_sends_died_to_all(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player1 = player_test_context1.player
            
            player_test_context2 = stack.enter_context(create_mock_player(self, 1))
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            
            player_test_context1.enter_room(room)
            player_test_context2.enter_room(room)
            
            room.on_player_suicide(player1)
            
            player_test_context1.assertHasReceivedMessageOfType('N_DIED')
            player_test_context2.assertHasReceivedMessageOfType('N_DIED')
            
    def test_on_suicide_player_becomes_dead(self):
        with mock_server_write_helper() as stack:
            player_test_context = stack.enter_context(create_mock_player(self, 0))
            player = player_test_context.player
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            player_test_context.enter_room(room)
            
            room.on_player_suicide(player)
            
            self.assertFalse(player.state.is_alive)
            
    def test_two_players_map_rotation(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player_test_context2 = stack.enter_context(create_mock_player(self, 1))
            
            ffa = gamemodes['ffa']
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            room.change_map_mode('complex', 'ffa')
            
            player_test_context1.enter_room(room)
            player_test_context2.enter_room(room)
            
            player_test_context1.clear_received_messages()
            player_test_context2.clear_received_messages()

            self.clock.advance(ffa.timeout)
            
            player_test_context1.assertHasReceivedMessageOfType('N_TIMEUP')
            messages = player_test_context1.get_received_messages_of_type('N_TIMEUP')
            self.assertEqual(messages[0]['timeleft'], 0)
            
            player_test_context1.clear_received_messages()
            player_test_context2.clear_received_messages()
            
            self.clock.advance(INTERMISSIONLEN)
            
            player_test_context1.assertHasReceivedMessageOfType('N_TIMEUP')
            messages = player_test_context1.get_received_messages_of_type('N_TIMEUP')
            self.assertEqual(messages[0]['timeleft'], ffa.timeout)
            
            #########################################################
            
            player_test_context1.clear_received_messages()
            player_test_context2.clear_received_messages()

            self.clock.advance(ffa.timeout)
            
            player_test_context1.assertHasReceivedMessageOfType('N_TIMEUP')
            messages = player_test_context1.get_received_messages_of_type('N_TIMEUP')
            self.assertEqual(messages[0]['timeleft'], 0)
            
            player_test_context1.clear_received_messages()
            player_test_context2.clear_received_messages()
            
            self.clock.advance(INTERMISSIONLEN)
            
            player_test_context1.assertHasReceivedMessageOfType('N_TIMEUP')
            messages = player_test_context1.get_received_messages_of_type('N_TIMEUP')
            self.assertEqual(messages[0]['timeleft'], ffa.timeout)
            
    def test_two_players_map_forced(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player_test_context2 = stack.enter_context(create_mock_player(self, 1))
            
            ffa = gamemodes['ffa']
            
            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            room.change_map_mode('complex', 'ffa')
            
            player_test_context1.enter_room(room)
            player_test_context2.enter_room(room)
            
            player_test_context1.clear_received_messages()
            player_test_context2.clear_received_messages()

            room.change_map_mode('complex', 'ffa')
            
            player_test_context1.assertHasReceivedMessageOfType('N_TIMEUP')
            messages = player_test_context1.get_received_messages_of_type('N_TIMEUP')
            self.assertEqual(messages[0]['timeleft'], ffa.timeout)
            
            #########################################################
            
            player_test_context1.clear_received_messages()
            player_test_context2.clear_received_messages()

            room.change_map_mode('complex', 'ffa')
            
            player_test_context1.assertHasReceivedMessageOfType('N_TIMEUP')
            messages = player_test_context1.get_received_messages_of_type('N_TIMEUP')
            self.assertEqual(messages[0]['timeleft'], ffa.timeout)
