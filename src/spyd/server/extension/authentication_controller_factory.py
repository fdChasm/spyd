from spyd.registry_manager import RegistryManager

import spyd.server.extension.authentication_controllers # @UnusedImport


class AuthenticationControllerFactory(object):
    def __init__(self, config):
        self._config = config

        authentication_type = config['type']

        self._AuthenticationController = None
        for transport_registration in RegistryManager.get_registrations('gep_authentication_controller'):
            controller_name = transport_registration.args[0]
            controller_class = transport_registration.registered_object

            if controller_name == authentication_type:
                self._AuthenticationController = controller_class
                break

        if self._AuthenticationController is None:
            raise Exception("Unknown general extension service authentication type specified; {!r}".format(authentication_type))

    def build_authentication_controller(self, protocol):
        return self._AuthenticationController(self._config, protocol)
