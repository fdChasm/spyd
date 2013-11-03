import unittest

from twisted.internet import task
from twisted.internet.defer import setDebugging

import spyd.game.room.room
from spyd.game.timing.game_clock import GameClock
from spyd.game.timing.resume_countdown import ResumeCountdown
from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from testing_utils.create_mock_player import create_mock_player
from testing_utils.protocol.mock_server_write_helper import mock_server_write_helper


class TestRoomMastermodes(unittest.TestCase):
    def setUp(self):
        self.clock = task.Clock()
        GameClock.clock = self.clock
        ScheduledCallbackWrapper.clock = self.clock
        ResumeCountdown.clock = self.clock

        setDebugging(True)

    def test_add_player_to_room_in_mastermode_2_joins_spectators(self):
        with mock_server_write_helper() as stack:
            player_test_context1 = stack.enter_context(create_mock_player(self, 0))
            player_test_context2 = stack.enter_context(create_mock_player(self, 1))

            room = spyd.game.room.room.Room(map_meta_data_accessor={})
            player_test_context1.enter_room(room)
            room.set_mastermode(mastermode=2)
            player_test_context2.enter_room(room)

            player_test_context2.assertHasReceivedMessageOfType('N_SPECTATOR')

            messages = player_test_context2.get_received_messages_of_type('N_SPECTATOR')

            message = messages[0]
            self.assertTrue(message['spectated'])
            self.assertEqual(message['client'], player_test_context2.player)
