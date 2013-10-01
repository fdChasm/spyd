from sauerpyd.map.map_meta_data_accessor import MapMetaDataAccessor
from sauerpyd.map.map_rotation import MapRotation
from sauerpyd.gamemode import gamemodes
import os

class RoomMapModeState(object):
    def __init__(self, room, map_rotation=None, map_meta_data_accessor=None):
        self.room = room
        self._map_name = ""
        self._gamemode = None
        self._map_meta_data_accessor = map_meta_data_accessor
        if self._map_meta_data_accessor is None:
            self._map_meta_data_accessor = MapMetaDataAccessor("{}/git/spyd/packages".format(os.environ['HOME']))
        self._map_rotation = map_rotation or MapRotation.from_test_data()
        self._initialized = False
        
    @property
    def initialized(self):
        return self._initialized
        
    @property
    def map_name(self):
        return self._map_name
    
    @property
    def gamemode(self):
        return self._gamemode
    
    @property
    def mode_num(self):
        return self._gamemode.clientmodenum
    
    @property
    def mode_name(self):
        return self._gamemode.clientmodename
    
    @property
    def map_meta_data(self):
        return self._map_meta_data_accessor.get(self._map_name, {})
    
    def get_map_names(self):
        return self._map_meta_data_accessor.get_map_names()
    
    @property
    def rotate_on_first_player(self):
        return self._map_rotation.rotate_on_first_player
    
    def rotate_map_mode(self):
        map_name, mode_name = self._map_rotation.next_map_mode(peek=False)
        self.change_map_mode(map_name, mode_name)
        
    def change_map_mode(self, map_name, mode_name):
        self._map_name = map_name
        self._gamemode = gamemodes[mode_name](room=self.room, map_meta_data=self.map_meta_data)
        self._initialized = True