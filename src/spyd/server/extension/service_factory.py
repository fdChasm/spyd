from spyd.registry_manager import RegistryManager
from spyd.server.extension.client_controller import ExtensionProtocolClientController
from spyd.server.extension.extension_service import GeneralExtensionService
from spyd.server.extension.protocol_factory import ExtensionProtocolFactory

import spyd.server.extension.packings # @UnusedImport
import spyd.server.extension.transports # @UnusedImport
from spyd.server.extension.authentication_controller_factory import AuthenticationControllerFactory


class GeneralExtensionServiceFactory(object):
    def __init__(self):
        self._transports = {}
        self._packings = {}

        for transport_registration in RegistryManager.get_registrations('gep_transport'):
            transport_name = transport_registration.args[0]
            transport_class = transport_registration.registered_object
            self._transports[transport_name] = transport_class

        for packing_registration in RegistryManager.get_registrations('gep_packing'):
            packing_name = packing_registration.args[0]
            packing_class = packing_registration.registered_object
            self._packings[packing_name] = packing_class

    def build_extension_service(self, spyd_server, config):
        transport_name = config.get('transport')
        packing_name = config.get('packing')

        TransportProtocol = self._transports[transport_name]
        packing = self._packings[packing_name]
        
        authentication = config.get('authentication')
        
        authentication_controller_factory = AuthenticationControllerFactory(authentication)

        factory = ExtensionProtocolFactory(spyd_server, TransportProtocol, packing, ExtensionProtocolClientController, authentication_controller_factory)

        interface = config.get('interface')
        port = config.get('port')

        return GeneralExtensionService(interface, port, factory)
