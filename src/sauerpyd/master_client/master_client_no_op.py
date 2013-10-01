from twisted.internet import defer, reactor
from sauerpyd.master_client.exceptions import AuthenticationFailure

class MasterClientNoOp(object):
    def try_auth(self, authname):
        deferred = defer.Deferred()
        exception = AuthenticationFailure("Could not determine which master server to send your request to.")
        reactor.callLater(0, deferred.errback, exception)
        return deferred
        
    def answer_challenge(self, auth_id, answer):
        deferred = defer.Deferred()
        exception = AuthenticationFailure("Could not determine which master server to send your request to.")
        reactor.callLater(0, deferred.errback, exception)
        return deferred