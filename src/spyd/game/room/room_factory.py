import os

from spyd.game.map.map_meta_data_accessor import MapMetaDataAccessor
from spyd.game.map.map_rotation import MapRotation, test_rotation_dict
from spyd.game.room.room import Room


class RoomFactory(object):
    """
    Initializes rooms from the config.
    If a room is in the room bindings section of the config it will be initialized with those settings.
    If a room type is specified the room will be initialized according to that registered room type if it exists.
    Otherwise it will be initialized with the default settings.
    """
    def __init__(self, config):
        self.config = config
        self.room_bindings = config.get('room_bindings', {})
        self.room_types = config.get('room_types', {})

    def build_room(self, name, room_type='default'):
        room_config = {}
        room_config.update(self.room_types.get(room_type, {}))
        room_config.update(self.room_bindings.get(name, {}))

        packages_directory = room_config.get('packages_directory', "{}/git/spyd/packages".format(os.environ['HOME']))
        map_meta_data_accessor = MapMetaDataAccessor(packages_directory)

        map_rotation_data = room_config.get('map_rotation', test_rotation_dict)
        map_rotation = MapRotation.from_dictionary(map_rotation_data)

        return Room(map_meta_data_accessor=map_meta_data_accessor, map_rotation=map_rotation)
