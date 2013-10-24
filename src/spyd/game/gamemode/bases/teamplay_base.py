from spyd.game.map.team import Team
from spyd.protocol import swh

base_teams = ('good', 'evil')

from cube2common.constants import client_states
class TeamplayBase(object):
    def __init__(self, room, map_meta_data):
        self.teams = {}
        for team_name in base_teams:
            self._get_team(team_name)

    def _get_team(self, name):
        if not name in self.teams:
            self.teams[name] = Team(len(self.teams), name)
        return self.teams[name]

    def initialize_player(self, cds, player):
        if player.state.state == client_states.CS_SPECTATOR: return
        possible_teams = filter(lambda t: t.size > 0 or t.name in base_teams, self.teams.values())
        smallest_team = min(possible_teams, key=lambda t: t.size)
        player.team = smallest_team
        player.team.size += 1
        swh.put_setteam(cds, player, -1)

    def on_player_disconnected(self, player):
        if player.team is not None:
            player.team.size -= 1
            player.team = None

    def on_player_try_set_team(self, player, target, old_team_name, new_team_name):
        team = self._get_team(new_team_name)
        if team is None: return

        if team is target.team: return

        self._teamswitch_suicide(target)
        with self.room.broadcastbuffer(1, True) as cds:
            if player is None:
                reason = -1
            elif player == target:
                reason = 0
            else:
                reason = 1
            target.team = team
            target.team.size += 1
            swh.put_setteam(cds, target, reason)

    def on_player_death(self, player, killer):
        pass

    def _teamswitch_suicide(self, player):
        if not player.state.is_alive: return
        player.state.suicide()
        player.state.respawn(self.room.gamemode)
        with self.room.broadcastbuffer(1, True) as cds:
            swh.put_died(cds, player, player)
        self.on_player_death(player, player)
