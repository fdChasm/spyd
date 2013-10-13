import enet
from twisted.internet.interfaces import IStreamServerEndpoint
from zope.interface import implements

from txENet.enet_host import ENetHost


class ENetServerEndpoint(object):
    implements(IStreamServerEndpoint)

    def __init__(self, reactor, interface, port, maxclients, channels, maxdown=0, maxup=0):
        self._reactor = reactor
        self._interface = interface
        self._port = port
        self._maxclients = maxclients
        self._channels = channels
        self._maxdown = maxdown
        self._maxup = maxup

        self._factory = None
        self._address = None
        self._enet_host = None

    def listen(self, factory):
        self._factory = factory

        self._address = enet.Address(self._interface, self._port)
        enet_host = enet.Host(self._address, self._maxclients, self._channels, self._maxdown, self._maxup)

        self._enet_host = ENetHost(enet_host, factory)

        self._reactor.addReader(self._enet_host)

    def flush(self):
        return self._enet_host.flush()
