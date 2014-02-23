import unittest

from twisted.internet import task

from mock import Mock
from spyd.authentication.exceptions import AuthFailedException
from spyd.authentication.services.vanilla import protocol_factory
from spyd.authentication.services.vanilla.protocol_factory import MasterClientProtocolFactory
from test_utils.deferreds import assertThrowsDeferred


class TestMasterClientProtocolFactory(unittest.TestCase):
    def setUp(self):
        self.clock = task.Clock()
        MasterClientProtocolFactory.clock = self.clock

        self.punitive_model = Mock()
        host = 'localhost'
        register_port = 28785
        self.instance = MasterClientProtocolFactory(self.punitive_model, host, register_port)

    def test_build_protocol(self):
        master_client_protocol = Mock()
        protocol_factory.MasterClientProtocol = Mock(return_value=master_client_protocol)
        self.assertEqual(self.instance.buildProtocol('127.0.0.1'), master_client_protocol)
        self.assertEqual(self.instance.active_connection, master_client_protocol)
        self.assertEqual(self.instance, master_client_protocol.factory)

    def test_connection_made(self):
        master_client_protocol = Mock()
        self.instance.active_connection = master_client_protocol
        self.instance.connectionMade(None)
        master_client_protocol.send_regserv.assert_called_once_with(28785)

    def test_connection_lost(self):
        connector = Mock()
        self.instance.clientConnectionLost(connector=connector, reason=None)

    def test_connection_failed(self):
        connector = Mock()
        self.instance.clientConnectionFailed(connector=connector, reason=None)

    def test_try_auth(self):
        master_client_protocol = Mock()
        self.instance.active_connection = master_client_protocol
        self.instance.try_auth('localhost', 'chasm')
        master_client_protocol.send_reqauth.assert_called_once_with(0, 'chasm')

    def test_try_auth_timeout(self):
        master_client_protocol = Mock()
        self.instance.active_connection = master_client_protocol
        d = self.instance.try_auth('localhost', 'chasm')
        self.clock.advance(5)
        assertThrowsDeferred(self, d, AuthFailedException)

    def test_answer_challenge(self):
        master_client_protocol = Mock()
        self.instance.active_connection = master_client_protocol
        d = self.instance.try_auth('localhost', 'chasm')

        self.instance.master_cmd_chalauth(['chalauth', 0, '+a5924762983dd70202bc2d9fca84042cd4507a57e62cff0f'])

        self.instance.answer_challenge(0, 'b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')
