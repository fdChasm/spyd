from twisted.internet.protocol import Factory

from spyd.server.binding.client_protocol import ClientProtocol
from txENet.enet_peer_transport import ENetPeerTransport


class ClientProtocolFactory(Factory):
    def __init__(self, client_factory, message_processor, message_rate_limit):
        self._client_factory = client_factory
        self._message_processor = message_processor
        self._message_rate_limit = message_rate_limit

        self._connected_protocols = set()

    def buildProtocol(self, enet_connect_event):
        peer = enet_connect_event.peer

        transport = ENetPeerTransport(peer)
        protocol = ClientProtocol(self._client_factory, self._message_processor, self._message_rate_limit)
        protocol.factory = self
        protocol.makeConnection(transport)
        return protocol

    def protocol_connected(self, protocol):
        self._connected_protocols.add(protocol)

    def protocol_disconnected(self, protocol):
        self._connected_protocols.discard(protocol)

    def disconnect_all(self, disconnect_type, message=None, timeout=3.0):
        for protocol in self._connected_protocols:
            protocol.disconnect_with_message(disconnect_type, message, timeout)
