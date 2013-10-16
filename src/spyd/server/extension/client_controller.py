from spyd.server.extension.exceptions import AuthenticationHardFailure


class ExtensionProtocolClientController(object):
    def __init__(self, spyd_server, client_addr, protocol, authentication_controller):
        self._spyd_server = spyd_server
        self._client_addr = client_addr
        self._protocol = protocol
        self._authentication_controller = authentication_controller

    @property
    def is_authenticated(self):
        return self._authentication_controller.is_authenticated

    def receive(self, message):
        print message
        if self.is_authenticated:
            self._receive_authenticated(message)
        else:
            self._receive_not_authenticated(message)

    def _receive_not_authenticated(self, message):
        try:
            self._authentication_controller.receive(message)
        except AuthenticationHardFailure:
            self._protocol.send({"msgtype": "error", "message": "Authentication failure"})
            self._protocol.disconnect()

    def _receive_authenticated(self, message):
        pass
