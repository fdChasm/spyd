from spyd.game.client.exceptions import UnknownPlayer, InsufficientPermissions
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


set_spectator_functionality = Functionality("spyd.game.room.set_spectator", 'Insufficient permissions to change your spectator status.')
set_other_spectator_functionality = Functionality("spyd.game.room.set_other_spectator", 'Insufficient permissions to change who is spectating.')
set_room_not_spectator_locked_functionality = Functionality("spyd.game.room.set_other_spectator", 'Insufficient permissions to unspectate when mastermode is locked.')

@register('room_client_event_handler')
class SetSpectatorHandler(object):
    event_type = 'set_spectator'

    @staticmethod
    def handle(room, client, target_pn, spectate):
        player = room.get_player(target_pn)
        if player is None:
            raise UnknownPlayer(cn=target_pn)

        if client.get_player() is player:
            if not client.allowed(set_spectator_functionality):
                raise InsufficientPermissions(set_spectator_functionality.denied_message)
            if not spectate and not client.allowed(set_room_not_spectator_locked_functionality):
                raise InsufficientPermissions(set_room_not_spectator_locked_functionality.denied_message)
        else:
            if not client.allowed(set_other_spectator_functionality):
                raise InsufficientPermissions(set_other_spectator_functionality.denied_message)

        room._set_player_spectator(player, spectate)
