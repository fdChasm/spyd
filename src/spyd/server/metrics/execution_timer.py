import contextlib
from twisted.internet import task, reactor


class ExecutionTimer(object):
    def __init__(self, metrics_service, metric_name, publish_interval, reactor=reactor):
        self._reactor = reactor
        self._metrics_service = metrics_service
        self._metric_name = metric_name
        self._publish_interval = publish_interval
        self._looping_call = task.LoopingCall(self._publish_metric)
        self._times = []
        self._started = False

    def _publish_metric(self):
        if not self._times: return
        average = sum(self._times) / float(len(self._times))
        self._metrics_service.publish_metric(self._metric_name, average, self._reactor.seconds())
        self._times = []

    def _ensure_started(self):
        if not self._started:
            self._looping_call.start(self._publish_interval)
            self._started = True

    @contextlib.contextmanager
    def measure(self):
        self._ensure_started()
        start_time = self._reactor.seconds()
        yield self
        end_time = self._reactor.seconds()
        metric_value = end_time - start_time
        self._times.append(metric_value)
