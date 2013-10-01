from cube2map.read_map_meta_data import read_map_data
import os.path
import glob

def map_filename_to_map_name(map_filename):
    return os.path.splitext(os.path.basename(map_filename))[0]

class MapMetaDataAccessor(object):
    def __init__(self, package_dir):
        self.package_dir = package_dir
        
        self._cached_map_meta = {}
        self._map_name_cache = None
        
    def get_map_path(self, map_name):
        map_filename = "{}.ogz".format(map_name)
        return os.path.join(self.package_dir, "base", map_filename)
    
    def get_map_data(self, map_name):
        map_path = self.get_map_path(map_name)
        return read_map_data(map_path)
        
    def __getitem__(self, map_name, default=None):
        if map_name not in self._cached_map_meta:
            self._cached_map_meta[map_name] = self.get_map_data(map_name)
        return self._cached_map_meta.get(map_name, default or {})
    
    def get(self, map_name, default=None):
        return self.__getitem__(map_name, default)
    
    def get_map_names(self, refresh=False):
        if self._map_name_cache is None or refresh:
            map_glob_expression = os.path.join(self.package_dir, "base", "*.ogz")
            map_filenames = glob.glob(map_glob_expression)
            self._map_name_cache = map(map_filename_to_map_name, map_filenames)
        return self._map_name_cache