class Subscription(object):
    def __init__(self, event_subscription_fulfiller, event_stream, event_handler):
        self._event_subscription_fulfiller = event_subscription_fulfiller
        self._event_stream = event_stream
        self._event_handler = event_handler

    def unsubscribe(self):
        self._event_subscription_fulfiller.unsubscribe(self._event_stream, self._event_handler)


class SubscriptionError(Exception): pass


class EventSubscriptionFulfiller(object):
    def __init__(self):
        # event_stream: set(handlers)
        self._subscriptions = {}

    def subscribe(self, event_stream, event_handler):
        if not event_stream in self._subscriptions:
            self._subscriptions[event_stream] = set()
        self._subscriptions[event_stream].add(event_handler)
        return Subscription(self, event_stream, event_handler)

    def unsubscribe(self, event_stream, event_handler):
        self._subscriptions.get(event_stream, set()).discard(event_handler)

    def publish(self, event_stream, data):
        for event_handler in self._subscriptions.get(event_stream, ()):
            try:
                event_handler(event_stream, data)
            except SubscriptionError:
                self.unsubscribe(event_stream, event_handler)
