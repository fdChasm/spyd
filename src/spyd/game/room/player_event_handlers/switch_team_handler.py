from spyd.registry_manager import register


@register('room_player_event_handler')
class SwitchTeamHandler(object):
    event_type = 'switch_team'

    @staticmethod
    def handle(room, player, team_name):
        room.gamemode.on_player_try_set_team(player, player, player.team.name, team_name)
