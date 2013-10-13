from twisted.internet import reactor
from twisted.application import service

carbon_client_missing = True
try:
    from txCarbonClient import CarbonClientService
    carbon_client_missing = False
except ImportError:
    pass

class NoOpRepeatingMetricHandle(object):
    def start(self):
        pass

    def stop(self):
        pass

class NoOpMetricService(service.Service):
    def __init__(self, reactor):
        pass

    def publish_metric(self, metric_name, metric_value, epoch_seconds=None):
        pass

    def register_repeating_metric(self, metric_name, frequency, getter):
        return NoOpRepeatingMetricHandle()

class PrefixingCarbonClientService(CarbonClientService):
    def __init__(self, reactor, hostname, port, prefix):
        self._prefix = prefix
        CarbonClientService.__init__(self, reactor, hostname, port)

    def publish_metric(self, metric_name, metric_value, epoch_seconds=None):
        metric_name = self._get_prefixed_metric_name(metric_name)
        return CarbonClientService.publish_metric(self, metric_name, metric_value, epoch_seconds)

    def _get_prefixed_metric_name(self, metric_name):
        return "{prefix}{metric_name}".format(prefix=self._prefix, metric_name=metric_name)

def get_metrics_service(config):
    config = config.get('carbon_metrics', {})

    enabled = config.get('enabled', False)
    carbon_host = config.get('host', 'localhost')
    carbon_port = config.get('port', 2004)
    metric_prefix = config.get('metric_prefix', 'spyd')

    if enabled and carbon_client_missing:
        print "Warning: could not import txCarbonClient package. No metrics will be recorded."
        enabled = False

    if enabled:
        carbon_client_service = PrefixingCarbonClientService(reactor, carbon_host, carbon_port, metric_prefix)
    else:
        carbon_client_service = NoOpMetricService(reactor)

    return carbon_client_service
