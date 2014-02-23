import unittest

from mock import Mock, call
from spyd.authentication.services import maestro_service
from spyd.authentication.services.maestro_service import MaestroMasterClientService


class TestMaestroMasterClientService(unittest.TestCase):
    def setUp(self):
        self.protocol_factory = Mock()

        self.tcp_client = Mock()

        self.TCPClient = Mock(return_value=self.tcp_client)
        maestro_service.TCPClient = self.TCPClient

    def test_build(self):
        maestro_master_client_service = Mock()
        MockMaestroMasterClientService = Mock(return_value=maestro_master_client_service)
        maestro_service.MaestroMasterClientService = MockMaestroMasterClientService

        maestro_protocol_factory = Mock()

        maestro_service.MaestroProtocolFactory = Mock(return_value=maestro_protocol_factory)

        punitive_model = Mock()
        config = Mock()
        config.get = Mock(side_effect=['localhost', 28787, 28785, ['localhost', '']])

        MaestroMasterClientService.build(punitive_model, config)

        config.get.assert_has_calls([call('host'), call('port'), call('register_port'), call('domains')])

        MockMaestroMasterClientService.assert_called_once_with(28787, maestro_protocol_factory, interface='localhost', domains=['localhost', ''])

    def test_instantiate(self):
        instance = self.make_instance()

        self.TCPClient.assert_called_once_with('localhost', 28787, self.protocol_factory)

        self.tcp_client.setServiceParent.assert_called_once_with(instance)

    def test_handles_domain(self):
        instance = self.make_instance()

        for domain in ['localhost', '']:
            self.assertTrue(instance.handles_domain(domain))
        for domain in [None, 'foo', 123]:
            self.assertFalse(instance.handles_domain(domain))

    def test_try_authenticate(self):
        instance = self.make_instance()

        instance.try_authenticate('localhost', 'chasm')

        self.protocol_factory.try_auth.assert_called_once_with('localhost', 'chasm')

    def test_answer_challenge(self):
        instance = self.make_instance()

        instance.answer_challenge('localhost', 43, 'b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')

        self.protocol_factory.answer_challenge.assert_called_once_with(43, 'b50ed38d434eb4d85f95ed83c7f54d27a98e7f1ab0c2dfe0')

    def make_instance(self):
        port = 28787
        interface = 'localhost'
        domains = ['localhost', '']

        return MaestroMasterClientService(port, self.protocol_factory, interface, domains)
