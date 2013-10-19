from spyd.game.map.map_rotation import MapRotation, test_rotation_dict
from spyd.game.room.room import Room


class RoomFactory(object):
    """
    Initializes rooms from the config.
    If a room is in the room bindings section of the config it will be initialized with those settings.
    If a room type is specified the room will be initialized according to that registered room type if it exists.
    Otherwise it will be initialized with the default settings.
    """
    def __init__(self, config, room_manager, server_name_model, map_meta_data_accessor, command_executer, event_subscription_fulfiller, metrics_service):
        self.config = config
        self.room_manager = room_manager
        self.room_manager.set_factory(self)
        
        self.room_bindings = config.get('room_bindings', {})
        self.room_types = config.get('room_types', {})
        self.server_name_model = server_name_model
        self.map_meta_data_accessor = map_meta_data_accessor
        self.command_executer = command_executer
        self.event_subscription_fulfiller = event_subscription_fulfiller
        self.metrics_service = metrics_service

    def build_room(self, name, room_type='default'):
        room_config = {}
        room_config.update(self.room_types.get(room_type, {}))
        room_config.update(self.room_bindings.get(name, {}))

        map_rotation_data = room_config.get('map_rotation', test_rotation_dict)
        map_rotation = MapRotation.from_dictionary(map_rotation_data)
        
        maxplayers = room_config.get('maxplayers', 12)

        room = Room(room_name=name,
                    room_manager=self.room_manager,
                    server_name_model=self.server_name_model, 
                    map_meta_data_accessor=self.map_meta_data_accessor, 
                    map_rotation=map_rotation,
                    command_executer=self.command_executer,
                    event_subscription_fulfiller=self.event_subscription_fulfiller,
                    maxplayers=maxplayers,
                    metrics_service=self.metrics_service)
        
        self.room_manager.add_room(room)
        
        return room
