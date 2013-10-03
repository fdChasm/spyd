'''
Holds a reference to a client and provides groups based on the room the client is currently in.
Returns 'local.room.master' group if the client is found in client.room.masters.
Returns 'local.room.admin' group if the client is found in client.room.admins. 
'''
class RoomGroupProvider(object):
    def __init__(self, client):
        self.client = client
        
    def get_group_names(self):
        group_names = []
        if self.client in self.client.room.masters:
            group_names.append('local.room.master')
        if self.client in self.client.room.admins:
            group_names.append('local.room.admin')
        return group_names
