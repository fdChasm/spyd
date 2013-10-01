import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)

from twisted.internet import defer, reactor
from twisted.protocols import basic

from cube2common.constants import AUTHCHALLEN
from sauerpyd.master_client.authentication_context import AuthenticationContext
from sauerpyd.master_client.constants import possible_commands, authentication_states
from sauerpyd.punitive_effects.punitive_effect_info import EffectInfo, PermaExpiryInfo
from sauerpyd.master_client.exceptions import AuthenticationFailure
from sauerpyd.client.master_server_authentication import MasterServerAuthentication

class MasterClientProtocol(basic.LineReceiver):
    delimiter = "\n"
    
    def lineReceived(self, line):
        logger.debug("Received master server command: {!r}".format(line))
        args = line.split(' ')
        if not len(args): return
        cmd = args[0]
        if not cmd in possible_commands: return
        handler_name = "master_cmd_{}".format(cmd)
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler(args)
        else:
            logger.error("Error no handler for master server command: {!r}".format(cmd))
            
    def sendLine(self, line):
        logger.debug("Sending master server command: {!r}".format(line))
        return basic.LineReceiver.sendLine(self, line)
            
    def connectionMade(self):
        basic.LineReceiver.connectionMade(self)
        self.register(self.factory.register_port)
            
    def register(self, port):
        request = "regserv {}".format(port)
        self.sendLine(request)
            
    def try_auth(self, authname):
        print "authname = {!r}".format(authname)
        context = AuthenticationContext(self.factory.get_next_auth_id(), authname)
        request = "reqauth {context.auth_id} {context.auth_name:.100s}".format(context=context)
        self.sendLine(request)
        self.factory.pending_auths[context.auth_id] = context
        context.timeout_deferred = reactor.callLater(5, self._auth_timeout, context)
        return context.deferred
    
    def answer_challenge(self, auth_id, answer):
        context = self.factory.pending_auths.get(auth_id, None)
        if context is None: return None
        
        if context.state is not authentication_states.PENDING_ANSWER:
            logger.error("Answer challenge called when another state was expected.")
            exception = AuthenticationFailure("Master server client protocol error.")
            return self._auth_failed(context, exception)

        request = "confauth {context.auth_id} {answer:.100s}".format(context=context, answer=answer)
        self.sendLine(request)
        context.state = authentication_states.PENDING_RESPONSE
        context.deferred = defer.Deferred()
        return context.deferred
    
    def _auth_timeout(self, context):
        exception = AuthenticationFailure("Authentication timed out.")
        self._auth_failed(context, exception)
    
    def _auth_failed(self, context, exception=None):
        exception = exception or AuthenticationFailure("Authentication failed.")
        if not context.deferred.called:
            context.deferred.errback(exception)
        self._auth_finished(context)
    
    def _auth_succeeded(self, context):
        authentication = MasterServerAuthentication(self.factory.host, context.auth_name)
        context.deferred.callback(authentication)
        self._auth_finished(context)

    def _auth_finished(self, context):
        if not context.timeout_deferred.called:
            context.timeout_deferred.cancel()
        if not context.deferred.called:
            context.deferred.cancel()
        del self.factory.pending_auths[context.auth_id]
    
    def master_cmd_succreg(self, args):
        logger.info("Successfully registered server with master server.")
        logger.debug('Master server resetting reconnection delay.')
        self.factory.resetDelay()

    def master_cmd_failreg(self, args):
        logger.info("Failed to register server with master server.")

    def master_cmd_addgban(self, args):
        effect_desc = args[1]
        effect_info = EffectInfo(PermaExpiryInfo())
        self.factory.punitive_model.add_effect('ban', effect_desc, effect_info)

    def master_cmd_cleargbans(self, args):
        self.factory.punitive_model.clear_effects('ban')

    def master_cmd_chalauth(self, args):
        auth_id = int(args[1])
        context = self.factory.pending_auths.get(auth_id, None)
        if context is None: return None
        
        if context.state is not authentication_states.PENDING_CHALLENGE:
            logger.error("Master server sent challenge when another state was expected.")
            exception = AuthenticationFailure("Master server protocol error.")
            return self._auth_failed(context, exception)
        
        challenge = args[2]
        
        if len(challenge) != AUTHCHALLEN:
            logger.error("Master server sent challenge with an invalid length of {}.".format(len(challenge)))
            exception = AuthenticationFailure("Master server protocol error.")
            return self._auth_failed(context, exception)
        
        context.state = authentication_states.PENDING_ANSWER
        context.deferred.callback((auth_id, challenge))

    def master_cmd_failauth(self, args):
        auth_id = int(args[1])
        context = self.factory.pending_auths.get(auth_id, None)
        if context is None: return None
        
        exception = AuthenticationFailure("Master server refused authentication attempt.")
        return self._auth_failed(context, exception)

    def master_cmd_succauth(self, args):
        auth_id = int(args[1])
        context = self.factory.pending_auths.get(auth_id, None)
        if context is None: return None
        
        if context.state is not authentication_states.PENDING_RESPONSE:
            logger.error("Master server sent authentication success when another state was expected.")
            exception = AuthenticationFailure("Master server protocol error.")
            return self._auth_failed(context, exception)
            
        self._auth_succeeded(context)