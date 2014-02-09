from spyd.protocol import swh

class SpawningBase(object):
    def __init__(self, room, map_meta_data):
        pass

    def on_player_request_spawn(self, player):
        if player.state.can_spawn:
            player.state.respawn()
            self.spawn_loadout(player)
            with player.sendbuffer(1, True) as cds:
                swh.put_spawnstate(cds, player)

    def spawn_loadout(self, player):
        player.state.health = self.spawnhealth
        player.state.armour = self.spawnarmour
        player.state.armourtype = self.spawnarmourtype
        player.state.gunselect = self.spawngunselect
        player.state.ammo = self.spawnammo
