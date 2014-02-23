import unittest
from spyd.authentication.services.vanilla.authentication_context import AuthChallenge, \
    AuthenticationContext


class TestAuthChallenge(unittest.TestCase):
    def setUp(self):
        pass

    def test_initial_state(self):
        instance = AuthChallenge(auth_id=0, auth_domain='localhost', challenge='b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')
        self.assertEqual(instance.auth_id, 0)
        self.assertEqual(instance.auth_domain, 'localhost')
        self.assertEqual(instance.challenge, 'b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')

class TestAuthenticationContext(unittest.TestCase):
    def setUp(self):
        pass

    def test_initial_state(self):
        instance = AuthenticationContext(auth_id=0, auth_domain='localhost', auth_name='chasm')
        self.assertEqual(instance.auth_id, 0)
        self.assertEqual(instance.auth_domain, 'localhost')
        self.assertEqual(instance.auth_name, 'chasm')
