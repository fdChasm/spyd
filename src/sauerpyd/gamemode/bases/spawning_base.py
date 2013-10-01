from sauerpyd.protocol import swh

class SpawningBase(object):
    def __init__(self, room, map_meta_data):
        pass

    def on_player_request_spawn(self, player):
        if player.state.can_spawn:
            player.state.respawn(self)
            with player.sendbuffer(1, True) as cds:
                swh.put_spawnstate(cds, player)
