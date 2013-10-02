from spyd.utils.match_fuzzy import match_fuzzy

class RoomManager(object):
    def __init__(self):
        self.rooms = {}
        
    def add_room(self, room):
        self.rooms[room.name] = room
        
    def get_room(self, name, fuzzy):
        if name in self.rooms:
            return self.rooms[name]
        elif fuzzy:
            name_match = match_fuzzy(name, self.rooms.keys())
            return self.rooms.get(name_match, None)
        