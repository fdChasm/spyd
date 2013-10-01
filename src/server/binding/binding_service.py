from twisted.application import service
from twisted.internet import reactor, task
import traceback

class BindingService(service.Service):
    def __init__(self, binding_factory):
        self.binding_factory = binding_factory
        self.binding_inits = []
        self.binding_protocols = set()
        
        reactor.addSystemEventTrigger('during', 'flush_bindings', self.flush_all)
        self.flush_looping_call = task.LoopingCall(reactor.fireSystemEvent, 'flush_bindings')
    
    def startService(self):
        for binding_init in self.binding_inits:
            binding_protocol = self.binding_factory.buildProtocol(None)
            reactor.spawnProcess(binding_protocol, binding_init[0], binding_init, None)
            self.binding_protocols.add(binding_protocol)
        service.Service.startService(self)
        
        self.flush_looping_call.start(0.033)
        
    def stopService(self):
        service.Service.stopService(self)
        
        self.flush_looping_call.stop()
        
    def add_binding(self, interface, port, maxclients, maxdown, maxup):
        binding_init = map(str, ('./binding_child.py', interface, port, maxclients, maxdown, maxup))
        self.binding_inits.append(binding_init)
        
    def flush_all(self):
        reactor.callLater(0, reactor.addSystemEventTrigger, 'during', 'flush_bindings', self.flush_all)
        try:
            for binding_protocol in self.binding_protocols:
                binding_protocol.send({'type': 'flush'})
        except:
            traceback.print_exc()
