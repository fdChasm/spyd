from mock import MagicMock
import unittest

from twisted.internet import task, reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

import logging
logging.basicConfig(level=logging.DEBUG)

from spyd.authentication.services.vanilla.protocol_factory import MasterClientProtocolFactory

'''
class TestRoomInstactf(unittest.TestCase):
    def setUp(self):
        self.clock = task.Clock()

    def test_first(self):

punitive_model_adapter = MagicMock()
protocol_factory = MasterClientProtocolFactory(punitive_model_adapter, 'localhost', 28785)

point = TCP4ClientEndpoint(reactor, "localhost", 28787)
d = point.connect(protocol_factory)

def gotChallenge(*arg):
    print "gotChallenge:", arg
    
def failAuth(*arg):
    print "failauth", arg

def gotProtocol(p):
    deferred = protocol_factory.try_auth('chasm')
    deferred.addCallback(gotChallenge)
    deferred.addErrback(failAuth)

d.addCallback(gotProtocol)

reactor.run()

'''