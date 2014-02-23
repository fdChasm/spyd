import unittest

from spyd.game.timing.scheduled_callback_wrapper import ScheduledCallbackWrapper
from twisted.internet import task
from twisted.internet.defer import setDebugging

class Test(unittest.TestCase):
    """Unit tests for ScheduledCallbackWrapper."""
    def setUp(self):
        self.clock = task.Clock()
        ScheduledCallbackWrapper.clock = self.clock
        setDebugging(True)

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
        
    def test_external_and_finished_callbacks(self):
        scheduled_callback_wrapper = ScheduledCallbackWrapper(5)
        scheduled_callback_wrapper.resume()
        self._finished_called = False
        self._timeup_called = False
        def on_finished_called(*args, **kwargs):
            self._finished_called = True
        def on_timeup_called(*args, **kwargs):
            self._timeup_called = True
        scheduled_callback_wrapper.add_finished_callback(on_finished_called)
        scheduled_callback_wrapper.add_timeup_callback(on_timeup_called)
        self.clock.advance(20)
        self.assertTrue(self._finished_called)
        self.assertTrue(self._timeup_called)
        
    def test_cancelling(self):
        scheduled_callback_wrapper = ScheduledCallbackWrapper(20)
        scheduled_callback_wrapper.resume()
        self._finished_called = False
        self._timeup_called = False
        def on_finished_called(*args, **kwargs):
            self._finished_called = True
        def on_timeup_called(*args, **kwargs):
            self._timeup_called = True
        scheduled_callback_wrapper.add_finished_callback(on_finished_called)
        scheduled_callback_wrapper.add_timeup_callback(on_timeup_called)

        self.clock.advance(15)
        self.assertFalse(self._finished_called)
        self.assertFalse(self._timeup_called)
        
        scheduled_callback_wrapper.cancel()

        self.assertTrue(self._finished_called)
        self.assertFalse(self._timeup_called)
        
        self.clock.advance(5)
        
        self.assertTrue(self._finished_called)
        self.assertFalse(self._timeup_called)

if __name__ == "__main__":
    unittest.main()
