import random

from cube2common.constants import item_types
from spyd.protocol import swh

class UnusedItemSlot(object):
    def __init__(self, index):
        self.index = 0
        self.type = 0
        self.spawned = False

class Item(object):
    def __init__(self, room, game_clock, index, item_type):
        self.room = room
        self.game_clock = game_clock
        
        self.index = index
        self.type = item_type
        self.spawn_deferred = None
        
        spawn_delay = self._spawn_delay()
        
        if spawn_delay is not None:
            self._schedule_spawn(spawn_delay)
            
    def __repr__(self):
        return "<Item index={}, spawned={}, type={}({})>".format(self.index, self.spawned, item_types.by_value(self.type), self.type)
            
    @property
    def spawned(self):
        return self.spawn_deferred is None
    
    def _spawn(self):
        self.spawn_deferred = None
        with self.room.broadcastbuffer(1, True) as cds:
            swh.put_itemspawn(cds, self)
            
    def _announce(self):
        self.spawn_announce_deferred = None
        with self.room.broadcastbuffer(1, True) as cds: 
            swh.put_announce(cds, self)

    def pickup(self, player):
        if not self.spawned: return
        if not player.state.pickup_item(self.type): return
        
        with self.room.broadcastbuffer(1, True) as cds: 
            swh.put_itemacc(cds, self, player)
            
        spawn_delay = self._respawn_delay()
        self._schedule_spawn(spawn_delay)

    def _spawn_delay(self):
        if self.type in [item_types.I_GREENARMOUR, item_types.I_YELLOWARMOUR, item_types.I_BOOST, item_types.I_QUAD]:
            return self._respawn_delay()
        else:
            return None

    def _respawn_delay(self):
        playercount = self.room.playing_count
        
        if playercount < 3:
            base = 4
        elif playercount in [3, 4]:
            base = 3
        elif playercount > 4:
            base = 2
            
        if self.type >= item_types.I_SHELLS and self.type <= item_types.I_CARTRIDGES:
            secs = base*4
        elif self.type == item_types.I_HEALTH:
            secs = base*5
        elif self.type == item_types.I_GREENARMOUR or self.type == item_types.I_YELLOWARMOUR:
            secs = 20
        elif self.type == item_types.I_BOOST or self.type == item_types.I_QUAD:
            secs = random.randint(40, 80)
        else:
            secs = 0
            
        return secs
    
    def _schedule_spawn(self, spawn_delay):
        self.spawn_deferred = self.game_clock.schedule_callback(spawn_delay)
        self.spawn_deferred.add_timeup_callback(self._spawn)
        
        if self.type in (item_types.I_QUAD, item_types.I_BOOST):
            self.spawn_announce_deferred = self.game_clock.schedule_callback(spawn_delay-10)
            self.spawn_announce_deferred.add_timeup_callback(self._announce)
        else:
            self.spawn_announce_deferred = None
