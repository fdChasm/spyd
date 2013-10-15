from twisted.internet import defer
from zope.interface import implements

from spyd.authentication.interfaces import IAuthChallenge
from spyd.authentication.services.vanilla.constants import authentication_states


class AuthChallenge(object):
    implements(IAuthChallenge)

    def __init__(self, auth_id, auth_domain, challenge):
        self.auth_id = auth_id
        self.auth_domain = auth_domain
        self.challenge = challenge

class AuthenticationContext(object):
    def __init__(self, auth_id, auth_domain, auth_name):
        self.auth_id = auth_id
        self.auth_domain = auth_domain
        self.auth_name = auth_name
        self.state = authentication_states.PENDING_CHALLENGE
        self.deferred = defer.Deferred()
        self.timeout_deferred = None
