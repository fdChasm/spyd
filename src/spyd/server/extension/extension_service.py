from twisted.application import service
from twisted.internet import reactor


class GeneralExtensionService(service.Service):
    def __init__(self, interface, port, protocol_factory):
        self._interface = interface
        self._port = port
        self._protocol_factory = protocol_factory
        
        self._listener = None

    def startService(self):
        self._listener = reactor.listenTCP(interface=self._interface, port=self._port, factory=self._protocol_factory)

    def stopService(self):
        return self._listener.stopListening()
