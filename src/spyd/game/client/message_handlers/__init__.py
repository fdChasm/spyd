from spyd.registry_manager import register, RegistryManager
from spyd.utils.import_all import import_all


import_all(__file__, 'spyd.game.client.message_handlers', ['__init__'])


def get_message_handlers():
    message_handlers = {}
    for registered_message_handler in RegistryManager.get_registrations('client_message_handler'):
        message_handler = registered_message_handler.registered_object
        message_type = message_handler.message_type
        message_handlers[message_type] = message_handler
    return message_handlers
