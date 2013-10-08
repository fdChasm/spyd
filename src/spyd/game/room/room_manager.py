from spyd.utils.match_fuzzy import match_fuzzy
from spyd.game.room.exceptions import RoomEntryFailure
from spyd.game.client.client_message_handling_base import GenericError
from spyd.game.server_message_formatter import info

class RoomManager(object):
    def __init__(self):
        self.rooms = {}
        self.room_factory = None
        
    def set_factory(self, room_factory):
        self.room_factory = room_factory

    def add_room(self, room):
        self.rooms[room.name] = room

    def get_room(self, name, fuzzy):
        if name in self.rooms:
            return self.rooms[name]
        elif fuzzy:
            name_match = match_fuzzy(name, self.rooms.keys())
            return self.rooms.get(name_match, None)

    def client_change_room(self, client, target_room):
        player = client.get_player()
        
        try:
            room_entry_context = target_room.get_entry_context(client, player)
        except RoomEntryFailure as e:
            raise GenericError(e.message)
        
        client.room._broadcaster.server_message(info("{name#client} is leaving to join {room#room}. Use {action#follow} to go there too.", client=client, room=target_room, follow="follow"), exclude=[client])
        
        client.room.client_leave(client)
        
        client.room.last_destination_room = target_room.name
        
        client.room = target_room
        
        target_room.client_enter(room_entry_context)
