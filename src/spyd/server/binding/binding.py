from txENet.enet_server_endpoint import ENetServerEndpoint


class Binding(ENetServerEndpoint):
    def __init__(self, reactor, metrics_service, interface, port, maxclients, channels, maxdown=0, maxup=0):
        metric_prefix = "{}.{}".format(interface.replace('.', '_'), port)

        received_metric_name = "{}.rx".format(metric_prefix)
        sent_metric_name = "{}.tx".format(metric_prefix)
        peer_count_metric_name = "{}.peer_count".format(metric_prefix)

        metrics_service.register_repeating_metric(received_metric_name, 1.0, self._get_and_reset_bytes_received)
        metrics_service.register_repeating_metric(sent_metric_name, 1.0, self._get_and_reset_bytes_sent)
        metrics_service.register_repeating_metric(peer_count_metric_name, 1.0, self._get_peer_count)

        ENetServerEndpoint.__init__(self, reactor, interface, port, maxclients, channels, maxdown=maxdown, maxup=maxup)

    def _get_and_reset_bytes_received(self):
        if self._enet_host is None: return 0
        try:
            return self._enet_host.total_received_data
        finally:
            self._enet_host.reset_total_received_data()

    def _get_and_reset_bytes_sent(self):
        if self._enet_host is None: return 0
        try:
            return self._enet_host.total_sent_data
        finally:
            self._enet_host.reset_total_sent_data()

    def _get_peer_count(self):
        if self._enet_host is None: return 0
        return self._enet_host.peer_count
