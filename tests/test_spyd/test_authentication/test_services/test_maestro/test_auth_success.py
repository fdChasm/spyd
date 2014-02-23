import unittest
from spyd.authentication.services.maestro.auth_success import MaestroAuthSuccess


class TestVanillaAuthSuccess(unittest.TestCase):
    def setUp(self):
        self.instance = MaestroAuthSuccess('localhost', 'chasm', 0, ['Administrator', 'Global_Admin'])
    
    def test_get_group_names(self):
        group_names = self.instance.group_provider.get_group_names()
        self.assertEqual(group_names, ['Administrator', 'Global_Admin', 'localhost.auth', 'chasm@localhost'])

    def test_repr(self):
        self.assertEqual(repr(self.instance.group_provider), '<MaestroAuthSuccess chasm@localhost>')
