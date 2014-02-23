from twisted.internet.protocol import Protocol


class NoCommaNetStringProtocol(Protocol):
    def __init__(self):
        self._buffer = bytearray()

    def dataReceived(self, data):
        self._buffer.extend(data)
        self._handle_messages()

    def _handle_messages(self):
        sep = self._buffer.find(':')
        while sep >= 0:
            length = int(self._buffer[:sep] or "0")
            if len(self._buffer) >= (length + sep + 1):
                message = self._buffer[sep + 1:length + sep + 1]
                self._buffer = self._buffer[length + sep + 1:]
                self.messageReceived(message)
            else:
                break
            sep = self._buffer.find(':')

    def sendMessage(self, message_data):
        msg_len = len(message_data)
        self.transport.write("{}:{}".format(msg_len, message_data))

    def messageReceived(self, message):
        raise NotImplemented()
