from cube2common.constants import mastermodes
from spyd.game.client.exceptions import InsufficientPermissions, GenericError
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


temporary_set_mastermode_functionality = Functionality("spyd.game.room.temporary.set_mastermode")
set_mastermode_functionality = Functionality("spyd.game.room.set_mastermode")

@register('room_client_event_handler')
class SetMasterModeHandler(object):
    event_type = 'set_master_mode'

    @staticmethod
    def handle(room, client, mastermode):
        allowed_set_mastermode = client.allowed(set_mastermode_functionality) or (room.temporary and client.allowed(temporary_set_mastermode_functionality))

        if not allowed_set_mastermode:
            raise InsufficientPermissions('Insufficient permissions to change mastermode.')

        if mastermode < mastermodes.MM_OPEN or mastermode > mastermodes.MM_PRIVATE:
            raise GenericError("Mastermode out of allowed range.")

        room.set_mastermode(mastermode)
