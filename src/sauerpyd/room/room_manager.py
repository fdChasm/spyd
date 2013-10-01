class RoomManager(object):
    def __init__(self):
        self.rooms = set()
        
    def add_room(self, room):
        self.rooms.add(room)