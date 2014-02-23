import unittest

from spyd.authentication.exceptions import AuthFailedException
from spyd.authentication.services.no_op import NoOpMasterClientService
from test_utils.deferreds import assertThrowsDeferred


class TestNoOpMasterClientService(unittest.TestCase):
    def setUp(self):
        self.nomcs = NoOpMasterClientService()

    def test_handles_domain(self):
        self.assertTrue(self.nomcs.handles_domain('localhost'))

    def test_try_authenticate(self):
        d = self.nomcs.try_authenticate('localhost', 'chasm')
        assertThrowsDeferred(self, d, AuthFailedException)

    def test_answer_challenge(self):
        d = self.nomcs.answer_challenge('localhost', 57, 'b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')
        assertThrowsDeferred(self, d, AuthFailedException)
