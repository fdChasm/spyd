from twisted.internet.protocol import ServerFactory
from server.binding.binding_protocol import BindingProtocol

class BindingFactory(ServerFactory):
    
    protocol = BindingProtocol
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        
    def message_received(self, binding_protocol, message):
        self.client_manager.message_received(binding_protocol, message)
