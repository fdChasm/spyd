from spyd.server.extension.central_message_handler import CentralMessageHandler
from spyd.server.extension.exceptions import AuthenticationHardFailure


class ExtensionProtocolClientController(object):
    def __init__(self, spyd_server, client_addr, protocol, authentication_controller):
        self._spyd_server = spyd_server
        self._client_addr = client_addr
        self._protocol = protocol
        self._authentication_controller = authentication_controller
        self._message_handler = CentralMessageHandler()
        
        self.event_subscriptions = []

    def send(self, message, respid=None):
        if respid is not None:
            message['respid'] = respid
        self._protocol.send(message)

    @property
    def is_authenticated(self):
        return self._authentication_controller.is_authenticated

    def get_group_names(self):
        return self._authentication_controller.groups

    def allowed(self, functionality):
        group_names = self.get_group_names()
        return self._spyd_server.permission_resolver.groups_allow(group_names, functionality)

    def receive(self, message):
        if self.is_authenticated:
            self._receive_authenticated(message)
        else:
            self._receive_not_authenticated(message)
            
    def disconnected(self):
        for event_subscription in self.event_subscriptions:
            event_subscription.unsubscribe()

    def _receive_not_authenticated(self, message):
        try:
            self._authentication_controller.receive(message)
        except AuthenticationHardFailure:
            self.send({"msgtype": "gep.error", "message": "Authentication failure"}, message.get('reqid', None))
            self._protocol.disconnect()

    def _receive_authenticated(self, message):
        try:
            self._message_handler.handle_message(self._spyd_server, self, message)
        except Exception as e:
            self.send({"msgtype": "error", "message": e.message}, message.get('reqid', None))
            
    def on_subscribed_event(self, event_stream, data):
        self.send({"msgtype": "gep.event", "event_stream": event_stream, "event_data": data})
