import unittest
from spyd.authentication.services.vanilla.auth_success import VanillaAuthSuccess


class TestVanillaAuthSuccess(unittest.TestCase):
    def setUp(self):
        self.instance = VanillaAuthSuccess('localhost', 'chasm')
    
    def test_get_group_names(self):
        group_names = self.instance.group_provider.get_group_names()
        self.assertEqual(group_names, ('localhost.auth', 'chasm@localhost'))

    def test_repr(self):
        self.assertEqual(repr(self.instance.group_provider), '<VanillaGroupProvider chasm@localhost>')
