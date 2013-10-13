from spyd.game.client.client import Client

class ClientFactory(object):
    def __init__(self, client_number_provider, room_bindings, master_client_bindings, permission_resolver):
        self.client_number_provider = client_number_provider
        self.room_bindings = room_bindings
        self.master_client_bindings = master_client_bindings
        self.permission_resolver = permission_resolver
    
    def build_client(self, client_protocol, binding_port):
        clientnum = self.client_number_provider.acquire_cn()
        
        room = self.room_bindings.get_room(binding_port)
        master_client = self.master_client_bindings.get_master_client(binding_port)
        
        return Client(client_protocol, clientnum, room, master_client, self.permission_resolver)
