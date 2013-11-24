import traceback

from cube2common.constants import disconnect_types
from spyd.game.client import message_handlers  # @UnusedImport
from spyd.game.client.exceptions import InsufficientPermissions, StateError, UsageError, GenericError
from spyd.game.server_message_formatter import denied, error, state_error, usage_error
from spyd.registry_manager import RegistryManager
from spyd.utils.constrain import ConstraintViolation


class ClientMessageHandlingBase(object):
    def __init__(self):
        self._ignored_preconnect_message_types = ("N_POS", "N_PING")
        self._allowed_preconnect_message_types = ("N_CONNECT", "N_AUTHANS")
        self._ignore_client_messages = False

        self._message_handlers = {}
        for registered_message_handler in RegistryManager.get_registrations('client_message_handler'):
            message_handler = registered_message_handler.registered_object
            message_type = message_handler.message_type
            self._message_handlers[message_type] = message_handler

    def _message_received(self, message_type, message):
        if self._ignore_client_messages: return
        try:
            if (not self.is_connected) and (message_type in self._ignored_preconnect_message_types):
                pass
            elif (not self.is_connected) and (message_type not in self._allowed_preconnect_message_types):
                print message_type
                self.disconnect(disconnect_types.DISC_MSGERR)
                return
            else:
                if message_type in self._message_handlers:
                    handler = self._message_handlers[message_type]
                    try:
                        handler.handle(self, self.room, message)
                    except InsufficientPermissions as e:
                        self.send_server_message(denied(e.message))
                    except StateError as e:
                        self.send_server_message(state_error(e.message))
                    except UsageError as e:
                        self.send_server_message(usage_error(e.message))
                    except GenericError as e:
                        self.send_server_message(error(e.message))
                    except ConstraintViolation as e:
                        print "Disconnecting client {} due to constraint violation {}.".format(self.host, e.constraint_name)
                        self.disconnect(disconnect_types.DISC_MSGERR)
                        return
                else:
                    print "Client received unhandled message type:", message_type, message
        except:
            traceback.print_exc()
            self.disconnect(disconnect_types.DISC_MSGERR)
            self._ignore_client_messages = True
