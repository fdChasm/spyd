from spyd.game.timing.expiry import Expiry
from spyd.protocol import swh

def multidispatched(func):
    base_func = func
    func_name = func.__name__
    def multidispatcher(self, *args, **kwargs):
        for base in self.__class__.__bases__:
            if base != ModeBase and hasattr(base, func_name):
                func = getattr(base, func_name)
                func(self, *args, **kwargs)
        base_func(self, *args, **kwargs)
    return multidispatcher

class ModeBase(object):
    @multidispatched
    def __init__(self, room, map_meta_data):
        self.room = room
        self.initialized = False
    
    @multidispatched
    def initialize(self):
        self.initialized = True
    
    @multidispatched
    def on_player_connected(self, player):
        pass
    
    @multidispatched
    def initialize_player(self, cds, player):
        pass
    
    @multidispatched
    def on_player_disconnected(self, player):
        pass
    
    @multidispatched
    def on_player_shoot(self, player, shot_id, gun, from_pos, to_pos, hits):
        pass
    
    @multidispatched
    def on_player_explode(self, player, cmillis, gun, explode_id, hits):
        pass
    
    @multidispatched
    def on_player_request_spawn(self, player):
        pass
    
    @multidispatched
    def on_player_death(self, player, killer):
        player.state.spawnwait = Expiry(self.room._game_clock, self.spawndelay)
    
    @multidispatched
    def on_client_flag_list(self, client, flag_list):
        pass
    
    @multidispatched
    def on_client_item_list(self, client, item_list):
        pass
    
    @multidispatched
    def on_client_base_list(self, client, base_list):
        pass
    
    @multidispatched
    def on_player_take_flag(self, player, flag_index, version):
        pass
    
    @multidispatched
    def on_player_try_drop_flag(self, player):
        pass
    
    @multidispatched
    def on_player_try_set_team(self, player, target, old_team_name, new_team_name):
        pass
    
    @multidispatched
    def on_player_pickup_item(self, player, item_index):
        pass
    
    @multidispatched
    def on_player_taunt(self, player):
        swh.put_taunt(player.state.messages)

    @multidispatched
    def on_player_spectate(self, player):
        pass

    @multidispatched
    def on_player_unspectate(self, player):
        pass
