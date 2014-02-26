import unittest
from spyd.permissions.functionality import Functionality


class TestFunctionality(unittest.TestCase):
    def test_functionality(self):
        f = Functionality('test', 'No access to test.')
        self.assertEqual(repr(f), "<Functionality: 'test'>")
