import unittest

from mock import Mock

from spyd.utils.observable import Observable


class TestObservable(unittest.TestCase):
    def setUp(self):
        self.observable = Observable()
        self.observer_method = Mock()

    def test_observe(self):
        self.observable.observe(self.observer_method)
        self.observable.notify()
        self.observer_method.assert_called_once_with(self.observable)

    def test_stop_observing(self):
        self.observable.observe(self.observer_method)
        self.observable.stop_observing(self.observer_method)
        self.observable.notify()
        self.assertEqual(self.observer_method.mock_calls, [])

    def test_stop_observing_using_observation(self):
        observation = self.observable.observe(self.observer_method)
        observation.stop_observing()
        self.observable.notify()
        self.assertEqual(self.observer_method.mock_calls, [])
