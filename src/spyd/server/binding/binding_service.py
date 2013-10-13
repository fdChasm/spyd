import traceback

from twisted.application import service
from twisted.internet import reactor, task
from spyd.server.metrics.rate_aggregator import RateAggregator


class BindingService(service.Service):
    def __init__(self, binding_factory, binding_path, metrics_service):
        self.binding_factory = binding_factory
        self.binding_inits = []
        self.binding_protocols = set()

        self.binding_child_path = binding_path
        
        self.metrics_service = metrics_service

        self.flush_rate_aggregator = RateAggregator(metrics_service, 'flush_all_rate', 1.0)

        reactor.addSystemEventTrigger('during', 'flush_bindings', self.flush_all)
        self.flush_looping_call = task.LoopingCall(reactor.fireSystemEvent, 'flush_bindings')

    def startService(self):
        for binding_init in self.binding_inits:
            binding_interface = binding_init[3].replace('.', '_')
            binding_identifier = '.'.join((binding_interface, binding_init[4]))
            write_rate_aggregator = RateAggregator(self.metrics_service, 'binding.{}.up'.format(binding_identifier), 1.0)
            read_rate_aggregator = RateAggregator(self.metrics_service, 'binding.{}.down'.format(binding_identifier), 1.0)
            binding_protocol = self.binding_factory.buildProtocol(write_rate_aggregator, read_rate_aggregator)
            reactor.spawnProcess(binding_protocol, self.binding_child_path, binding_init, None)
            self.binding_protocols.add(binding_protocol)
        service.Service.startService(self)

        self.flush_looping_call.start(0.033)

    def stopService(self):
        service.Service.stopService(self)

        self.flush_looping_call.stop()

    def add_binding(self, interface, port, maxclients, maxdown, maxup):
        binding_init = map(str, (self.binding_child_path, interface, port, maxclients, maxdown, maxup))
        self.binding_inits.append(binding_init)

    def flush_all(self):
        reactor.callLater(0, reactor.addSystemEventTrigger, 'during', 'flush_bindings', self.flush_all)
        try:
            for binding_protocol in self.binding_protocols:
                binding_protocol.send({'type': 'flush'})
            self.flush_rate_aggregator.tick()
        except:
            traceback.print_exc()
