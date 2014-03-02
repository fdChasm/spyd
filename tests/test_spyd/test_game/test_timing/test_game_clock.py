import unittest

from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from twisted.internet import task
from spyd.game.timing.game_clock import GameClock
from spyd.game.timing.resume_countdown import ResumeCountdown

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
        
    def test_timeleft_before_resume(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        self.assertAlmostEqual(game_clock.timeleft, 600)
        
    def test_timeleft_after_resume(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        game_clock.resume(0)
        self.clock.advance(0)
        self.assertAlmostEqual(game_clock.timeleft, 600)
        
    def test_timeleft_after_resume_and_20_sec(self):
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

    def test_callback_not_called_if_cancelled(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        game_clock.resume(None)
        self._was_called = False
        def func():
            self._was_called = True

        scheduled_callback_wrapper = game_clock.schedule_callback(5)

        scheduled_callback_wrapper.add_timeup_callback(func)

        game_clock.cancel()

        self.clock.advance(10)

        self.assertFalse(self._was_called)

    def test_start_then_set_timeleft(self):
        game_clock = GameClock()
        game_clock.start(600, 10)
        game_clock.resume(None)

        game_clock.timeleft = 300
        self.assertEqual(game_clock.timeleft, 300)

    def test_start_untimed(self):
        game_clock = GameClock()
        game_clock.start_untimed()
        game_clock.resume(None)
        self.assertEqual(game_clock.timeleft, 0)
        self.clock.advance(20)
        self.assertEqual(game_clock.timeleft, 0)
