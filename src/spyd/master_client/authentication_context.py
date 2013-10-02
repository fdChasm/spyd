from twisted.internet import defer

from spyd.master_client.constants import authentication_states


class AuthenticationContext(object):
    def __init__(self, auth_id, auth_name):
        self.auth_id = auth_id
        self.auth_name = auth_name
        self.state = authentication_states.PENDING_CHALLENGE
        self.deferred = defer.Deferred()
        self.timeout_deferred = None
