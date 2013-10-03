from spyd.game.client.client import Client
from spyd.server.client_protocol_wrapper import ClientProtocolWrapper

class ClientFactory(object):
    
    def __init__(self, client_number_provider, room_bindings, master_client_bindings, permission_resolver):
        self.client_number_provider = client_number_provider
        self.room_bindings = room_bindings
        self.master_client_bindings = master_client_bindings
        self.permission_resolver = permission_resolver
    
    def build_client(self, binding_protocol, connect_message):
        clientnum = self.client_number_provider.acquire_cn()
        identifier = connect_message['ident']
        host = connect_message['host']
        port = connect_message['port']
        
        binding_port = connect_message.get('binding', {}).get('port', None)
        room = self.room_bindings.get_room(binding_port)
        master_client = self.master_client_bindings.get_master_client(binding_port)
        
        protocol_wrapper = ClientProtocolWrapper(binding_protocol, identifier)
        
        return Client(identifier, protocol_wrapper, host, port, clientnum, room, master_client, self.permission_resolver)
