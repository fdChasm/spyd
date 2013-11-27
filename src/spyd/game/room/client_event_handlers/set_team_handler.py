from spyd.game.client.exceptions import InsufficientPermissions, UnknownPlayer
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


set_others_teams_functionality = Functionality("spyd.game.room.set_others_teams", 'Insufficient permissions to change other players teams.')

@register('room_client_event_handler')
class SetTeamHandler(object):
    event_type = 'set_team'

    @staticmethod
    def handle(room, client, target_pn, team_name):
        if not client.allowed(set_others_teams_functionality):
            raise InsufficientPermissions(set_others_teams_functionality.denied_message)

        player = room.get_player(target_pn)
        if player is None:
            raise UnknownPlayer(cn=target_pn)

        room.gamemode.on_player_try_set_team(client.get_player(), player, player.team.name, team_name)
