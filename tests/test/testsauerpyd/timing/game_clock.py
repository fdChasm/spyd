import unittest

from sauerpyd.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from twisted.internet import task
from sauerpyd.timing.game_clock import GameClock
from sauerpyd.timing.resume_countdown import ResumeCountdown

class Test(unittest.TestCase):
    """Unit tests for ScheduledCallbackWrapper."""
    def setUp(self):
        self.clock = task.Clock()
        GameClock.clock = self.clock
        ScheduledCallbackWrapper.clock = self.clock
        ResumeCountdown.clock = self.clock
        
    def test_initialize(self):
        game_clock = GameClock()
        self.assertEqual(game_clock.timeleft, 0.0)
        
    def test_resume_paused_changes(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        self.assertTrue(game_clock.is_paused)
        game_clock.resume(0)
        self.clock.advance(0)
        self.assertFalse(game_clock.is_paused)
        
    def test_time_elapsed_before_resume(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        self.assertAlmostEqual(game_clock.timeleft, 600)
        
    def test_time_elapsed_after_resume(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        game_clock.resume(0)
        self.clock.advance(0)
        self.assertAlmostEqual(game_clock.timeleft, 600)
        
    def test_time_elapsed_after_resume_and_20_sec(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        game_clock.resume(0)
        self.clock.advance(0)
        self.clock.advance(20)
        self.assertAlmostEqual(game_clock.timeleft, 580)
        
    def test_intermission_start_timeleft_0(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        game_clock.resume(0)
        self.clock.advance(0)
        self.clock.advance(605)
        self.assertAlmostEqual(game_clock.timeleft, 0)
        
    def test_intermission_5_sec_in_remaining(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        game_clock.resume(0)
        self.clock.advance(0)
        self.clock.advance(605)
        self.assertAlmostEqual(game_clock.intermission_timeleft, 5)