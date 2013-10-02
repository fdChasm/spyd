import cube2common.cube_data_stream
import contextlib
from spyd.game.player.player import Player

class ClientCollection(object):
    def __init__(self):
        #cn: client
        self._clients = {}
        
    def add(self, client):
        self._clients[client.cn] = client
        
    def remove(self, client):
        del self._clients[client.cn]
    
    def to_list(self):
        return self._clients.values()
    
    def to_iterator(self):
        return self._clients.itervalues()
    
    def by_cn(self, cn):
        return self._clients[cn]
    
    def broadcast(self, channel, data, reliable=False, exclude=None, clients=None):
        clients = clients or self._clients.itervalues()
        exclude = set(exclude or ())
        for v in tuple(exclude):
            if isinstance(v, Player):
                exclude.add(v.client)
        for client in clients:
            if not client in exclude:
                client.send(channel, data, reliable)

    @contextlib.contextmanager
    def broadcastbuffer(self, channel, reliable=False, exclude=[], clients=None):
        cds = cube2common.cube_data_stream.CubeDataStream()
        yield cds
        self.broadcast(channel, cds, reliable, exclude, clients)