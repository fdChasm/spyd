
test_rotation_dict = {
    'rotations': {
                  'instactf': ['forge', 'dust2'],
                  'ffa': ['complex'],
                  'coop': ['ot'],
                  'traitors': ['ot'],
		  'insta': ['ot'],
                 },
    'modes': ['insta', 'traitors', 'ffa', 'coop', 'instactf']
}

class MapRotation(object):
    @staticmethod
    def from_dictionary(dictionary):
        return MapRotation(dictionary['rotations'],
                           dictionary['modes'],
                           dictionary.get('rotate_modes', False),
                           dictionary.get('rotate_on_first_player', False))
        
    @staticmethod
    def from_test_data():
        return MapRotation.from_dictionary(test_rotation_dict)
    
    def __init__(self, map_rotation_dict, mode_rotation_list, rotate_modes=False, rotate_on_first_player=False):
        self.map_rotation_dict = map_rotation_dict
        self.mode_rotation_list = mode_rotation_list
        self.rotate_modes = rotate_modes
        self.rotate_on_first_player = rotate_on_first_player
        
        self.mode_index = 0
        self.map_index = -1
    
    def next_map_mode(self, peek):
        this_mode_name = self.mode_rotation_list[self.mode_index]
        this_mode_maps = self.map_rotation_dict[this_mode_name]
        map_index = self.map_index + 1
        mode_index = self.mode_index
        
        if map_index >= len(this_mode_maps):
            map_index = 0
            if self.rotate_modes:
                mode_index = (mode_index + 1) % len(self.mode_rotation_list)
                this_mode_name = self.mode_rotation_list[mode_index]
                this_mode_maps = self.map_rotation_dict[this_mode_name]
        
        if not peek:
            self.map_index = map_index
            self.mode_index = mode_index
    
        return this_mode_maps[map_index], this_mode_name
