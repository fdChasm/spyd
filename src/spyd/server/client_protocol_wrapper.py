class ClientProtocolWrapper(object):
    def __init__(self, protocol, identifier):
        self.protocol = protocol
        self.identifier = identifier
        
    def send(self, channel, data, reliable):
        cmd = {'type': 'send', 'ident': self.identifier, 'channel': channel, 'data': data, 'reliable': reliable}
        return self.protocol.send(cmd)
        
    def disconnect(self, disconnect_type, wait=False):
        cmd = {'type': 'disconnect', 'ident': self.identifier, 'dt': disconnect_type, 'wait': wait}
        return self.protocol.send(cmd)
    
    def flush(self):
        return self.protocol.send({'type': 'flush'})