class PlayerNetworkBase(object):
    def __init__(self, client):
        self.client = client
        
    def send(self, channel, data, reliable):
        return self.client.send(channel, data, reliable)
    
    def send_server_message(self, message):
        self.client.send_server_message(message)
        
    @property
    def sendbuffer(self):
        return self.client.sendbuffer