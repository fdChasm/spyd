import unittest

from mock import Mock
from spyd.authentication.auth_world_view import AuthWorldView
from spyd.authentication.exceptions import AuthFailedException
from test_utils.deferreds import assertThrowsDeferred


class TestAuthWorldView(unittest.TestCase):
    def setUp(self):
        pass

    def test_no_services_throws(self):
        awv = AuthWorldView([])
        d = awv.try_authenticate('localhost', 'chasm')
        assertThrowsDeferred(self, d, AuthFailedException)

    def test_simple_domain_not_handled(self):
        auth_service = Mock()
        auth_service.handles_domain = Mock(return_value=False)

        awv = AuthWorldView([auth_service])

        d = awv.try_authenticate('localhost', 'chasm')

        auth_service.handles_domain.assert_called_once_with('localhost')

        assertThrowsDeferred(self, d, AuthFailedException)

    def test_simple_authentication_case(self):
        auth_service = Mock()
        auth_service.handles_domain = Mock(return_value=True)

        awv = AuthWorldView([auth_service])

        awv.try_authenticate('localhost', 'chasm')

        auth_service.handles_domain.assert_called_once_with('localhost')
        auth_service.try_authenticate.assert_called_once_with('localhost', 'chasm')

    def test_simple_answer_challenge_case(self):
        auth_service = Mock()
        auth_service.handles_domain = Mock(return_value=True)

        awv = AuthWorldView([auth_service])

        awv.answer_challenge('localhost', 57, 'b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')

        auth_service.handles_domain.assert_called_once_with('localhost')
        auth_service.answer_challenge.assert_called_once_with('localhost', 57, 'b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')
