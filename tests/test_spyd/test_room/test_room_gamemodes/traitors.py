import unittest

from twisted.internet import task

import spyd.game.room.room
from spyd.game.timing.game_clock import GameClock
from spyd.game.timing.resume_countdown import ResumeCountdown
from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from testing_utils.complex_meta_data import complex_meta_data
from testing_utils.create_mock_player import create_mock_player
from testing_utils.protocol.mock_server_write_helper import mock_server_write_helper


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
            room.change_map_mode('complex', 'traitors')

            player_test_context.enter_room(room)