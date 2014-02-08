import enet


class ENetPeerTransport(object):
    def __init__(self, enet_peer):
        self._enet_peer = enet_peer

    def send(self, channel, data, reliable, no_allocate=False):
        flags = 0
        if reliable: flags |= enet.PACKET_FLAG_RELIABLE
        if no_allocate: flags |= enet.PACKET_FLAG_NO_ALLOCATE
        packet = enet.Packet(data, flags)
        return self._enet_peer.send(channel, packet)

    def disconnect(self, reason):
        self._enet_peer.disconnect(reason)

    @property
    def host(self):
        return self._enet_peer.address.host

    @property
    def port(self):
        return self._enet_peer.address.port

    @property
    def connected_port(self):
        return self._enet_peer.host.address.port
