import enet
from twisted.internet.interfaces import IReadWriteDescriptor
from zope.interface import implements


handled_enet_events = (enet.EVENT_TYPE_CONNECT, enet.EVENT_TYPE_DISCONNECT, enet.EVENT_TYPE_RECEIVE)

class ENetHost(object):
    implements(IReadWriteDescriptor)

    def __init__(self, enet_host, factory):
        self._enet_host = enet_host
        self._client_protocol_factory = factory

        self._client_protocols = {}

    def doWrite(self):
        self._service_host()

    def doRead(self):
        self._service_host()

    def _service_host(self):
        while True:
            event = self._enet_host.service(0)

            if not event.type in handled_enet_events: return

            identifier = event.peer.incomingSessionID, event.peer.incomingPeerID

            if event.type == enet.EVENT_TYPE_CONNECT:
                client_protocol = self._client_protocol_factory.buildProtocol(event)
                self._client_protocols[identifier] = client_protocol

            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                if identifier in self._client_protocols:
                    client_protocol = self._client_protocols[identifier]
                    del self._client_protocols[identifier]
                    client_protocol.connectionLost(None)

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                if identifier in self._client_protocols:
                    client_protocol = self._client_protocols[identifier]
                    client_protocol.receiveEventReceived(event)

    def connectionLost(self, failure):
        pass

    def fileno(self):
        return self._enet_host.socket.fileno()

    def logPrefix(self):
        return ""

    def flush(self):
        return self._enet_host.flush()

    @property
    def peer_count(self):
        return len(self._client_protocols)

    @property
    def total_sent_data(self):
        return self._enet_host.totalSentData

    def reset_total_sent_data(self):
        self._enet_host.totalSentData = 0

    @property
    def total_sent_packets(self):
        return self._enet_host.totalSentPackets

    def reset_total_sent_packets(self):
        self._enet_host.totalSentPackets = 0

    @property
    def total_received_data(self):
        return self._enet_host.totalReceivedData

    def reset_total_received_data(self):
        self._enet_host.totalReceivedData = 0

    @property
    def total_peceived_packets(self):
        return self._enet_host.totalReceivedPackets

    def reset_total_peceived_packets(self):
        self._enet_host.totalReceivedPackets = 0
