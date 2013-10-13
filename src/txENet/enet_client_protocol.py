from twisted.internet.protocol import Protocol


class ENetClientProtocol(Protocol):
    def receiveEventReceived(self, event):
        self.dataReceived(event.channelID, event.packet.data)

    def connectionMade(self):
        pass

    def dataReceived(self, channel, data):
        pass
