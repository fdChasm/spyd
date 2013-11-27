from spyd.utils.import_all import import_all
import_all(__file__, 'spyd.game.room.player_event_handlers', ['__init__'])

from spyd.registry_manager import RegistryManager


def get_player_event_handlers():
    player_event_handlers = {}
    for registered_event_handler in RegistryManager.get_registrations('room_player_event_handler'):
        event_handler = registered_event_handler.registered_object
        event_type = event_handler.event_type
        player_event_handlers[event_type] = event_handler
    return player_event_handlers
