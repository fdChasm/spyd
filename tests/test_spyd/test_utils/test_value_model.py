import unittest

from mock import Mock

from spyd.utils.value_model import ValueModel


class TestValueModel(unittest.TestCase):
    def setUp(self):
        self.value_model = ValueModel('0')
        self.observer_method = Mock()

    def test_initial_value(self):
        self.assertEqual(self.value_model.value, '0')

    def test_change_value(self):
        self.value_model.value = '1'
        self.assertEqual(self.value_model.value, '1')

    def test_observe(self):
        self.value_model.observe(self.observer_method)
        self.value_model.value = '1'
        self.observer_method.assert_called_once_with(self.value_model)

    def test_stop_observing(self):
        self.value_model.observe(self.observer_method)
        self.value_model.stop_observing(self.observer_method)
        self.value_model.value = '1'
        self.assertEqual(self.observer_method.mock_calls, [])

    def test_stop_observing_using_observation(self):
        observation = self.value_model.observe(self.observer_method)
        observation.stop_observing()
        self.value_model.value = '1'
        self.assertEqual(self.observer_method.mock_calls, [])
