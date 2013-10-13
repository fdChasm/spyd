class RateAggregator(object):
    def __init__(self, metrics_service, metric_name, publish_interval):
        self._count = 0
        self._handle = metrics_service.register_repeating_metric(metric_name, publish_interval, self._get_and_clear_count)

    def tick(self, count=1):
        self._count += count

    def stop(self):
        self._handle.stop()

    def _get_and_clear_count(self):
        count = self._count
        self._count = 0
        return count
