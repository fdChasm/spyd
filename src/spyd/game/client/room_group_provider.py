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
        
        room = self.client.room
        
        if self.client in room.masters:
            group_names.append('local.room.master')
        if self.client in room.auths:
            group_names.append('local.room.auth')
        if self.client in room.admins:
            group_names.append('local.room.admin')
            
        #if room.get_client(self.client.cn) is not None:
        group_names.append('local.client')
            
        return group_names
