from twisted.internet.protocol import Factory

class ExtensionProtocolFactory(Factory):
    def __init__(self, spyd_server, TransportProtocol, packing, ExtensionProtocolController, authentication_controller_factory):
        self._spyd_server = spyd_server
        self._TransportProtocol = TransportProtocol
        self._packing = packing
        self._ExtensionProtocolController = ExtensionProtocolController
        self._authentication_controller_factory = authentication_controller_factory

    def buildProtocol(self, addr):
        protocol = self._TransportProtocol(self._packing)
        authentication_controller = self._authentication_controller_factory.build_authentication_controller(protocol)
        controller = self._ExtensionProtocolController(self._spyd_server, addr, protocol, authentication_controller)

        protocol.controller = controller
        protocol.factory = self

        return protocol
