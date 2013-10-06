from twisted.internet import defer

from spyd.protocol import swh
from spyd.game.server_message_formatter import error


class ClientAuthableBase(object):
    def __init__(self, master_client):
        self.master_client = master_client
        self.auth_deferred = None
        
    def auth(self, authdomain, authname):
        if self.auth_deferred is not None:
            self.send_server_message(error("You already have a pending auth request wait for the previous one to complete."))
            return
        
        self.auth_deferred = defer.Deferred()
        
        deferred = self.master_client.try_auth(authname)
        
        deferred.addCallback(self.on_auth_challenge)
        deferred.addErrback(self.on_auth_failure)
        
        return self.auth_deferred
    
    def answer_auth_challenge(self, authdomain, authid, answer):
        if self.auth_deferred is None:
            return
        
        deferred = self.master_client.answer_challenge(authid, answer)
        
        deferred.addCallback(self.on_auth_success)
        deferred.addErrback(self.on_auth_failure)
        
    def on_auth_challenge(self, challenge_info):
        auth_id, challenge = challenge_info

        with self.sendbuffer(1, True) as cds:
            swh.put_authchall(cds, "", auth_id, challenge)
    
    def on_auth_failure(self, deferred_exception):
        self.send_server_message(error(deferred_exception.value.message))
        self.auth_deferred.errback(deferred_exception)
        
    def on_auth_success(self, authentication):
        if authentication is not None:
            self.add_group_name_provider(authentication)
        
        self.auth_deferred.callback(authentication)
