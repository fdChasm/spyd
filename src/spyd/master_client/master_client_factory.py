import logging

from twisted.internet.protocol import ReconnectingClientFactory

from spyd.master_client.master_client_protocol import MasterClientProtocol


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)


class MasterClientFactory(ReconnectingClientFactory):
    def __init__(self, punitive_model, host, register_port):
        self.host = host
        self.punitive_model = punitive_model
        self.register_port = register_port
        
        self.pending_auths = {}
        self._next_auth_id = 0
        
        self.active_connection = None
        
    def get_next_auth_id(self):
        authid = self._next_auth_id
        self._next_auth_id += 1
        return authid
    
    def startedConnecting(self, connector):
        logger.debug('Master started to connect.')

    def buildProtocol(self, addr):
        logger.debug('Master server connected.')
        self.active_connection = MasterClientProtocol()
        self.active_connection.factory = self
        return self.active_connection

    def clientConnectionLost(self, connector, reason):
        logger.debug('Lost connection.  Reason: {!r}'.format(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logger.debug('Connection failed.  Reason: {!r}'.format(reason))
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        
    def try_auth(self, authname):
        return self.active_connection.try_auth(authname)
        
    def answer_challenge(self, auth_id, answer):
        return self.active_connection.answer_challenge(auth_id, answer)
