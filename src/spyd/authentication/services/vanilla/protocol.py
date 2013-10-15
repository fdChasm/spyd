import logging

from twisted.protocols import basic
from spyd.authentication.services.vanilla.constants import possible_commands


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)


class MasterClientProtocol(basic.LineReceiver):
    delimiter = "\n"

    def lineReceived(self, line):
        logger.debug("Received master server command: {!r}".format(line))
        args = line.split(' ')
        if not len(args): return
        cmd = args[0]
        if not cmd in possible_commands: return
        handler_name = "master_cmd_{}".format(cmd)
        if hasattr(self.factory, handler_name):
            handler = getattr(self.factory, handler_name)
            handler(args)
        else:
            logger.error("Error no handler for master server command: {!r}".format(cmd))

    def sendLine(self, line):
        logger.debug("Sending master server command: {!r}".format(line))
        return basic.LineReceiver.sendLine(self, line)

    def connectionMade(self):
        basic.LineReceiver.connectionMade(self)
        self.factory.connectionMade(self)

    def send_regserv(self, port):
        request = "regserv {}".format(port)
        self.sendLine(request)
        
    def send_reqauth(self, auth_id, auth_name):
        request = "reqauth {auth_id} {auth_name:.100s}".format(auth_id=auth_id, auth_name=auth_name)
        self.sendLine(request)
        
    def send_confauth(self, auth_id, answer):
        request = "confauth {auth_id} {answer:.100s}".format(auth_id=auth_id, answer=answer)
        self.sendLine(request)
