from twisted.internet import defer
from zope.interface import implements

from spyd.authentication.exceptions import AuthFailedException
from spyd.authentication.interfaces import IAuthService


class AuthWorldView(object):
    '''Represents the collection of authentication services available to a given client.
    Implements the interface of an Auth Service, but distributes requests and answers based on the
    auth_domain.
    '''
    implements(IAuthService)

    def __init__(self, auth_services):
        self._auth_services = auth_services

    def try_authenticate(self, auth_domain, auth_name):
        auth_service = self._get_auth_service(auth_domain)
        if auth_service is None: return defer.fail(AuthFailedException("Could not determine which master server to send your request to."))
        return auth_service.try_authenticate(auth_domain, auth_name)

    def answer_challenge(self, auth_domain, auth_id, answer):
        auth_service = self._get_auth_service(auth_domain)
        if auth_service is None: return defer.fail(AuthFailedException("Could not determine which master server to send your request to."))
        return auth_service.answer_challenge(auth_domain, auth_id, answer)

    def _get_auth_service(self, auth_domain):
        for auth_service in self._auth_services:
            if auth_service.handles_domain(auth_domain):
                return auth_service
        return None
