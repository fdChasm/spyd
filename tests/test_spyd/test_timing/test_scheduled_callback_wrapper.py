import unittest

from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from twisted.internet import task

class Test(unittest.TestCase):
    """Unit tests for ScheduledCallbackWrapper."""
    def setUp(self):
        self.clock = task.Clock()
        ScheduledCallbackWrapper.clock = self.clock

    def test_timeleft_before_started(self):
        """Test that the amount of time left is correct before actually starting the scheduled callback."""
        scheduled_callback_wrapper = ScheduledCallbackWrapper(5)
        self.assertEqual(scheduled_callback_wrapper.timeleft, 5.0)
        
    def test_timeleft_after_2_seconds(self):
        scheduled_callback_wrapper = ScheduledCallbackWrapper(5)
        scheduled_callback_wrapper.resume()
        self.clock.advance(2)
        self.assertAlmostEqual(scheduled_callback_wrapper.timeleft, 3.0)
        
    def test_timeleft_after_20_seconds(self):
        scheduled_callback_wrapper = ScheduledCallbackWrapper(5)
        scheduled_callback_wrapper.resume()
        self.clock.advance(20)
        self.assertAlmostEqual(scheduled_callback_wrapper.timeleft, 0.0)
        
    def test_external_and_internal_callbacks(self):
        scheduled_callback_wrapper = ScheduledCallbackWrapper(5)
        scheduled_callback_wrapper.resume()
        self._internal_called = False
        self._external_called = False
        def on_internal_called(*args, **kwargs):
            self._internal_called = True
        def on_external_called(*args, **kwargs):
            self._external_called = True
        scheduled_callback_wrapper.internal_deferred.addCallback(on_internal_called)
        scheduled_callback_wrapper.external_deferred.addCallback(on_external_called)
        self.clock.advance(20)
        self.assertTrue(self._internal_called)
        self.assertTrue(self._external_called)

if __name__ == "__main__":
    unittest.main()