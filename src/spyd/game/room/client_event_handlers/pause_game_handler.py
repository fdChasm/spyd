from spyd.game.client.exceptions import InsufficientPermissions, StateError
from spyd.game.server_message_formatter import info
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


pause_resume_functionality = Functionality("spyd.game.room.pause_resume", 'Insufficient permissions to pause or resume the game.')

@register('room_client_event_handler')
class PauseGameHandler(object):
    event_type = 'pause_game'

    @staticmethod
    def handle(room, client, pause):
        if not client.allowed(pause_resume_functionality):
            raise InsufficientPermissions(pause_resume_functionality.denied_message)

        if pause:
            if room.is_paused and not room.is_resuming: raise StateError('The game is already paused.')
            room.pause()
            room._broadcaster.server_message(info("{name#client} has paused the game.", client=client))
        elif not pause:
            if not room.is_paused: raise StateError('The game is already resumed.')
            room.resume()
            room._broadcaster.server_message(info("{name#client} has resumed the game.", client=client))
