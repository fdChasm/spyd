import traceback

from twisted.application import service
from twisted.internet import reactor, task

from spyd.server.binding.binding import Binding
from spyd.server.metrics.rate_aggregator import RateAggregator


class BindingService(service.Service):
    def __init__(self, client_protocol_factory, metrics_service):
        self.bindings = set()

        self.client_protocol_factory = client_protocol_factory

        self.metrics_service = metrics_service

        self.flush_rate_aggregator = RateAggregator(metrics_service, 'flush_all_rate', 1.0)

        reactor.addSystemEventTrigger('during', 'flush_bindings', self.flush_all)
        self.flush_looping_call = task.LoopingCall(reactor.fireSystemEvent, 'flush_bindings')

    def startService(self):
        for binding in self.bindings:
            binding.listen(self.client_protocol_factory)

        self.flush_looping_call.start(0.033)

        service.Service.startService(self)

    def stopService(self):
        self.flush_looping_call.stop()
        service.Service.stopService(self)

    def add_binding(self, interface, port, maxclients, maxdown, maxup):
        binding = Binding(reactor, self.metrics_service, interface, port, maxclients=maxclients, channels=2, maxdown=maxdown, maxup=maxup)
        self.bindings.add(binding)

    def flush_all(self):
        reactor.callLater(0, reactor.addSystemEventTrigger, 'during', 'flush_bindings', self.flush_all)
        try:
            for binding in self.bindings:
                binding.flush()
            self.flush_rate_aggregator.tick()
        except:
            traceback.print_exc()
