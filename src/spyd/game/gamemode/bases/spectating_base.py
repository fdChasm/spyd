from spyd.protocol import swh

class SpectatingBase(object):
    def __init__(self, room, map_meta_data):
        self.room = room
    
    def _spectate_suicide(self, cds, player):
        if not player.state.is_alive: return
        self.on_player_death(player, player)

    def on_player_spectate(self, player):
        with self.room.broadcastbuffer(1, True) as cds:
            self._spectate_suicide(cds, player)
            player.state.is_spectator = True
            swh.put_spectator(cds, player)

    def on_player_unspectate(self, player):
        with self.room.broadcastbuffer(1, True) as cds:
            player.state.is_spectator = False
            self.initialize_player(cds, player)
            self.on_player_connected(player)
            player.state.respawn(self)
            swh.put_spectator(cds, player)
