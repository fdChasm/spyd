import unittest

from mock import Mock
from spyd.authentication.services.vanilla import punitive_model_adapter
from spyd.authentication.services.vanilla.punitive_model_adapter import PunitiveModelAdapter


class TestPunitiveModelAdapter(unittest.TestCase):
    def setUp(self):
        self.effect_info = Mock()
        punitive_model_adapter.EffectInfo = Mock(return_value=self.effect_info)
        self.punitive_model = Mock()
        self.pma = PunitiveModelAdapter(self.punitive_model)

    def test_add_ban(self):
        effect_desc = "127.0.0.1"
        self.pma.add_ban(effect_desc)
        self.punitive_model.add_effect.assert_called_once_with('ban', effect_desc, self.effect_info)

    def test_clear_bans(self):
        self.pma.clear_bans()
        self.punitive_model.clear_effects.assert_called_once_with('ban')
