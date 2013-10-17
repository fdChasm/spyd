# This is the Twisted Get Poetry Now! client, version 7.0

import optparse, sys, json

from twisted.internet import defer
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver

class GEPProtocol(NetstringReceiver):

    def stringReceived(self, data):
        print "received", data
        
        
    def connectionMade(self):
        Protocol.connectionMade(self)
        self.sendString(json.dumps({"msgtype": "connect", "username": "bob", "domain": "example.com"}))

    def connectionLost(self, reason):
        print "connection lost"


class GEPClientFactory(ClientFactory):

    protocol = GEPProtocol


def poetry_main():

    from twisted.internet import reactor

    host, port = "127.0.0.1", 28788
    
    factory = GEPClientFactory()
    reactor.connectTCP(host, port, factory)

    reactor.run()

if __name__ == '__main__':
    poetry_main()
