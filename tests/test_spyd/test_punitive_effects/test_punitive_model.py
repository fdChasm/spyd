import unittest

from spyd.punitive_effects.punitive_model import PunitiveModel
from mock import Mock


class TestPunitiveModel(unittest.TestCase):
    def setUp(self):
        self.ban_effect = Mock()
        self.mute_effect = Mock()
        self.punitive_model = PunitiveModel()

    def test_simple_no_masking(self):
        self.punitive_model.add_effect('ban', '127.0.0.1', self.ban_effect)
        self.assertEqual(self.punitive_model.get_effect('ban', '127.0.0.1'), self.ban_effect)

    def test_simple_masking(self):
        self.punitive_model.add_effect('ban', '127.0.0', self.ban_effect)
        self.assertEqual(self.punitive_model.get_effect('ban', '127.0.0.1'), self.ban_effect)

    def test_arbitrary_mask(self):
        self.punitive_model.add_effect('ban', ('127.0.0.1', '0.255.255.255'), self.ban_effect)
        self.assertEqual(self.punitive_model.get_effect('ban', '33.0.0.1'), self.ban_effect)

    def test_clearing_bans(self):
        self.punitive_model.add_effect('ban', '127.0.0.1', self.ban_effect)
        self.punitive_model.clear_effects('ban')
        self.assertEqual(self.punitive_model.get_effect('ban', '127.0.0.1'), None)

    def test_different_effect_types(self):
        self.punitive_model.add_effect('ban', '127.0.0.1', self.ban_effect)
        self.punitive_model.add_effect('mute', '127.0.0.1', self.mute_effect)
        self.assertEqual(self.punitive_model.get_effect('ban', '127.0.0.1'), self.ban_effect)
        self.assertEqual(self.punitive_model.get_effect('mute', '127.0.0.1'), self.mute_effect)
