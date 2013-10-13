from twisted.internet.protocol import ServerFactory

from spyd.server.binding.binding_protocol import BindingProtocol


class BindingFactory(ServerFactory):
    def __init__(self, client_manager):
        self.client_manager = client_manager
        
    def buildProtocol(self, write_rate_aggregator, read_rate_aggregator):
        protocol = BindingProtocol(write_rate_aggregator, read_rate_aggregator)
        protocol.factory = self
        return protocol
        
    def message_received(self, binding_protocol, message):
        self.client_manager.message_received(binding_protocol, message)
