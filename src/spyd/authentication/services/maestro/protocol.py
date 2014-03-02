import json
import logging

from spyd.authentication.services.maestro.no_comma_netstring_protocol import NoCommaNetStringProtocol
from spyd.authentication.services.vanilla.constants import possible_commands


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)


class MaestroProtocol(NoCommaNetStringProtocol):

    def messageReceived(self, message_data):
        logger.debug("Recieved master server response: {!r}".format(str(message_data)))

        message = json.loads(str(message_data))

        cmd = message.pop('cmd')

        if not cmd in possible_commands: return
        handler_name = "master_cmd_{}".format(cmd)
        if hasattr(self.factory, handler_name):
            handler = getattr(self.factory, handler_name)
            handler(**message)
        else:
            logger.error("Error no handler for master server command: {!r}".format(cmd))

    def sendRequest(self, request):
        message_data = json.dumps(request)
        logger.debug("Sending master server command: {!r}".format(message_data))
        return self.sendMessage(message_data)

    def connectionMade(self):
        self.factory.connectionMade(self)

    def send_regserv(self, port):
        pass

    def send_reqauth(self, auth_id, auth_name):
        request = {"cmd": "reqauth", "reqid": auth_id, "authname": auth_name}
        self.sendRequest(request)

    def send_confauth(self, auth_id, answer):
        request = {"cmd": "confauth", "reqid": auth_id, "answer": answer}
        self.sendRequest(request)
