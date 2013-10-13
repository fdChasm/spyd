from twisted.internet.protocol import Factory

from txENet.enet_client_protocol import ENetClientProtocol
from txENet.enet_peer_transport import ENetPeerTransport


class ENetClientProtocolFactory(Factory):
    protocol = ENetClientProtocol

    def buildProtocol(self, enet_connect_event):
        transport = ENetPeerTransport(enet_connect_event.peer)
        protocol = self.protocol()
        protocol.factory = self
        protocol.makeConnection(transport)
        return protocol
