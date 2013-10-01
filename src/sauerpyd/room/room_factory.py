from sauerpyd.room.room import Room

#TODO: Implement

class RoomFactory(object):
    """
    Initializes rooms from the config.
    If a room is in the room bindings section of the config it will be initialized with those settings.
    If a room type is specified the room will be initialized according to that registered room type if it exists.
    Otherwise it will be initialized with the default settings.
    """
    def __init__(self, config):
        self.config = config
        
    def build_room(self, name, room_type='default'):
        return Room()