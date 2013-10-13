from twisted.internet import reactor
from twisted.internet.protocol import Factory, connectionDone

from txENet.enet_client_protocol import ENetClientProtocol
from txENet.enet_client_protocol_factory import ENetClientProtocolFactory
from txENet.enet_server_endpoint import ENetServerEndpoint


class ClientProtocol(ENetClientProtocol):
    def connectionMade(self):
        print "connection made!"

    def dataReceived(self, channel, data):
        print "data received"

    def connectionLost(self, reason=connectionDone):
        print "connection lost"
        ENetClientProtocol.connectionLost(self, reason=reason)


class ClientFactory(ENetClientProtocolFactory):
    protocol = ClientProtocol


endpoint = ENetServerEndpoint(reactor, '127.0.0.1', 28785, maxclients=24, channels=2, maxdown=0, maxup=0)
client_factory = ClientFactory()
endpoint.listen(client_factory)

reactor.run()
