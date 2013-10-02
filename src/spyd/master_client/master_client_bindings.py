from spyd.master_client.master_client_no_op import MasterClientNoOp

class MasterClientBindings(object):
    '''
    Associates master clients and ports for the purpose of determining which master client
    should be associated with a newly connected client
    '''
    def __init__(self):
        #port: room
        self.master_client_bindings = {}
        
        #room: port
        self.master_client_port = {}
        
        self.default_master_client = MasterClientNoOp()
        
    def add_master_client(self, port, master_client, default=False):
        self.master_client_bindings[port] = master_client
        if not master_client in self.master_client_port:
            self.master_client_port[master_client] = set()
        self.master_client_port[master_client].add(port)
        
        if default:
            self.default_master_client = master_client
        
    def get_master_client(self, port):
        return self.master_client_bindings.get(port, None) or self.default_master_client

    def get_port(self, master_client):
        return self.master_client_port.get(master_client, None)

    def remove_binding(self, port):
        if port in self.master_client_bindings:
            master_client = self.master_client_bindings.pop(port)
            del self.master_client_port[master_client]

    def remove_master_client(self, master_client):
        if master_client in self.master_client_port:
            port = self.master_client_port.pop(master_client)
            del self.master_client_bindings[port]
