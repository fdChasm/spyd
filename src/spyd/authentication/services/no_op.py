from twisted.application import service
from twisted.internet import defer
from zope.interface import implements

from spyd.authentication.exceptions import AuthFailedException
from spyd.authentication.interfaces import IAuthService
from spyd.game.registry_manager import register


@register("master_client_service", "no_op")
class NoOpMasterClientService(service.Service):
    implements(IAuthService)
    
    def handles_domain(self, auth_domain):
        return True
    
    def try_authenticate(self, auth_domain, auth_name):
        return defer.fail(AuthFailedException("Could not determine which master server to send your request to."))

    def answer_challenge(self, auth_domain, auth_id, answer):
        return defer.fail(AuthFailedException("Could not determine which master server to send your request to."))
