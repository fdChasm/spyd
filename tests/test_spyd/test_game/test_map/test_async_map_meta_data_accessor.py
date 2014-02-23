from spyd.game.map.async_map_meta_data_accessor import AsyncMapMetaDataAccessor
from twisted.internet import reactor

map_meta_data_accessor = AsyncMapMetaDataAccessor(package_dir="/opt/sauerbraten/packages")

map_name_index = 0

def on_error(err):
    print err

def on_map_names(map_names):
    global map_name_index
    map_count = len(map_names)

    def on_map_data(map_data):
        print map_data
        global map_name_index
        map_name_index = (map_name_index + 1) % map_count
        map_name = map_names[map_name_index]
        print map_name
        reactor.callLater(0, lambda: map_meta_data_accessor.get_map_data(map_name).addCallbacks(on_map_data, on_error))

    map_name_index = (map_name_index + 1) % map_count
    map_name = map_names[map_name_index]
    print map_name
    map_meta_data_accessor.get_map_data(map_name).addCallbacks(on_map_data, on_error)

reactor.callLater(0, lambda: map_meta_data_accessor.get_map_names().addCallback(on_map_names))
reactor.run()
