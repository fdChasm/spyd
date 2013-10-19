from spyd.registry_manager import RegistryManager

import spyd.server.extension.message_handlers  # @UnusedImport
from spyd.permissions.functionality import Functionality

class UnknownMessageHandler(object):
    execute = Functionality('gep.unknown_message')
    
    @staticmethod
    def handle_message(spyd_server, gep_client, message):
        raise Exception("Unknown msgtype {!r} received.".format(message.get('msgtype', None)))

class CentralMessageHandler(object):
    def __init__(self):
        self._message_handlers = {}

        for message_handler_registration in RegistryManager.get_registrations('gep_message_handler'):
            message_handler = message_handler_registration.registered_object
            if message_handler.msgtype in self._message_handlers:
                raise Exception("Duplicate message handler registered.")
            self._message_handlers[message_handler.msgtype] = message_handler

    def _get_message_handler(self, message):
        msgtype = message.get('msgtype')
        return self._message_handlers.get(msgtype, UnknownMessageHandler)

    def handle_message(self, spyd_server, gep_client, message):
        message_handler = self._get_message_handler(message)
        if not gep_client.allowed(message_handler.execute):
            raise Exception("Permission denied.")
        message_handler.handle_message(spyd_server, gep_client, message)
