import logging

from twisted.internet.protocol import ReconnectingClientFactory
from spyd.authentication.services.vanilla.protocol import MasterClientProtocol
from spyd.authentication.exceptions import AuthFailedException
from spyd.authentication.services.vanilla.constants import authentication_states
from cube2common.constants import AUTHCHALLEN
from twisted.internet import defer, reactor
from spyd.authentication.services.vanilla.authentication_context import AuthenticationContext,\
    AuthChallenge
import itertools
from spyd.authentication.services.vanilla.auth_success import VanillaAuthSuccess



logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)


class MasterClientProtocolFactory(ReconnectingClientFactory):
    def __init__(self, punitive_model, host, register_port):
        self.host = host
        self.punitive_model = punitive_model
        self.register_port = register_port

        self.noisy = False

        self.pending_auths = {}
        self._auth_id = itertools.count()

        self.active_connection = None

    def startedConnecting(self, connector):
        logger.debug('Master started to connect.')

    def buildProtocol(self, addr):
        logger.debug('Master server connected.')
        self.active_connection = MasterClientProtocol()
        self.active_connection.factory = self
        return self.active_connection
    
    def connectionMade(self, protocol):
        self.active_connection.send_regserv(self.register_port)

    def clientConnectionLost(self, connector, reason):
        logger.debug('Lost connection.  Reason: {!r}'.format(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logger.debug('Connection failed.  Reason: {!r}'.format(reason))
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def try_auth(self, auth_domain, authname):
        logger.debug("Attempting client auth request; authname = {!r}".format(authname))
        context = AuthenticationContext(self._auth_id.next(), auth_domain, authname)
        self.active_connection.send_reqauth(context.auth_id, context.auth_name)
        self.pending_auths[context.auth_id] = context
        context.timeout_deferred = reactor.callLater(5, self._auth_timeout, context)
        return context.deferred

    def answer_challenge(self, auth_id, answer):
        context = self.pending_auths.get(auth_id, None)
        if context is None: return None

        if context.state is not authentication_states.PENDING_ANSWER:
            logger.error("Answer challenge called when another state was expected.")
            exception = AuthFailedException("Master server client protocol error.")
            return self._auth_failed(context, exception)

        self.active_connection.send_confauth(auth_id, answer)
        context.state = authentication_states.PENDING_RESPONSE
        context.deferred = defer.Deferred()
        return context.deferred

    def _auth_timeout(self, context):
        exception = AuthFailedException("Authentication timed out.")
        self._auth_failed(context, exception)

    def _auth_failed(self, context, exception=None):
        exception = exception or AuthFailedException("Authentication failed.")
        if not context.deferred.called:
            context.deferred.errback(exception)
        self._auth_finished(context)

    def _auth_succeeded(self, context):
        authentication = VanillaAuthSuccess(self.host, context.auth_name)
        context.deferred.callback(authentication)
        self._auth_finished(context)

    def _auth_finished(self, context):
        if not context.timeout_deferred.called:
            context.timeout_deferred.cancel()
        if not context.deferred.called:
            context.deferred.cancel()
        del self.pending_auths[context.auth_id]

    def master_cmd_succreg(self, args):
        logger.info("Successfully registered server with master server.")
        logger.debug('Master server resetting reconnection delay.')
        self.resetDelay()

    def master_cmd_failreg(self, args):
        logger.info("Failed to register server with master server.")

    def master_cmd_addgban(self, args):
        self.punitive_model.add_ban(args[1])

    def master_cmd_cleargbans(self, args):
        self.punitive_model.clear_bans()

    def master_cmd_chalauth(self, args):
        auth_id = int(args[1])
        context = self.pending_auths.get(auth_id, None)
        if context is None: return None

        if context.state is not authentication_states.PENDING_CHALLENGE:
            logger.error("Master server sent challenge when another state was expected.")
            exception = AuthFailedException("Master server protocol error.")
            return self._auth_failed(context, exception)

        challenge = args[2]

        if len(challenge) != AUTHCHALLEN:
            logger.error("Master server sent challenge with an invalid length of {}.".format(len(challenge)))
            exception = AuthFailedException("Master server protocol error.")
            return self._auth_failed(context, exception)

        context.state = authentication_states.PENDING_ANSWER
        auth_challenge = AuthChallenge(auth_id, context.auth_domain, challenge)
        context.deferred.callback(auth_challenge)

    def master_cmd_failauth(self, args):
        auth_id = int(args[1])
        context = self.pending_auths.get(auth_id, None)
        if context is None: return None

        exception = AuthFailedException("Master server refused authentication attempt.")
        return self._auth_failed(context, exception)

    def master_cmd_succauth(self, args):
        auth_id = int(args[1])
        context = self.pending_auths.get(auth_id, None)
        if context is None: return None

        if context.state is not authentication_states.PENDING_RESPONSE:
            logger.error("Master server sent authentication success when another state was expected.")
            exception = AuthFailedException("Master server protocol error.")
            return self._auth_failed(context, exception)

        self._auth_succeeded(context)
