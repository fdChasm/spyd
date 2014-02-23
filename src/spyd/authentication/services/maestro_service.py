from twisted.application import service
from twisted.application.internet import TCPClient
from zope.interface import implements

from spyd.authentication.interfaces import IAuthService
from spyd.authentication.services.maestro.protocol_factory import MaestroProtocolFactory
from spyd.authentication.services.maestro.punitive_model_adapter import PunitiveModelAdapter
from spyd.registry_manager import register


@register("master_client_service", "maestro")
class MaestroMasterClientService(service.MultiService):
    implements(IAuthService)

    @staticmethod
    def build(punitive_model, config):
        host = config.get('host')
        port = config.get('port')
        register_port = config.get('register_port')
        domains = config.get('domains')

        punitive_model_adapter = PunitiveModelAdapter(punitive_model)

        protocol_factory = MaestroProtocolFactory(punitive_model_adapter, host, register_port)

        return MaestroMasterClientService(port, protocol_factory, interface=host, domains=domains)

    def __init__(self, port, factory, interface='', domains=[]):
        service.MultiService.__init__(self)

        self._protocol_factory = factory
        self._domains = domains

        self._child_service = TCPClient(interface, port, factory)
        self._child_service.setServiceParent(self)

    def handles_domain(self, auth_domain):
        return auth_domain in self._domains

    def try_authenticate(self, auth_domain, auth_name):
        return self._protocol_factory.try_auth(auth_domain, auth_name)

    def answer_challenge(self, auth_domain, auth_id, answer):
        return self._protocol_factory.answer_challenge(auth_id, answer)
