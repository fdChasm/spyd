class RoomBindings(object):
    '''
    Associates rooms and ports for the purpose of determining which room
    a client should go to when first connecting.
    '''
    def __init__(self):
        #port: room
        self.room_bindings = {}
        
        #room: set(port1, port2,...)
        self.room_ports = {}
        
        self.default_room = None
        
    def add_room(self, port, room, default=False):
        self.room_bindings[port] = room
        if not room in self.room_ports:
            self.room_ports[room] = set()
        self.room_ports[room].add(port)
        
        if default:
            self.default_room = room
        
    def get_room(self, port):
        return self.room_bindings.get(port, None) or self.default_room
    
    def get_ports(self, room):
        return tuple(self.room_ports.get(room, ()))
    
    def remove_binding(self, port):
        if port in self.room_bindings:
            room = self.room_bindings.pop(port)
            del self.room_ports[room]
            
    def remove_room(self, room):
        if room in self.room_ports:
            ports = self.room_ports.pop(room)
            while len(ports):
                port = ports.pop()
                del self.room_bindings[port]
