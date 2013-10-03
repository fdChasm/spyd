class InvalidPlayerNumberReference(Exception): pass

class ClientBase(object):
    def __init__(self, clientnum, room):
        self.cn = clientnum
        self.room = room
        self.players = {}
        
    @property
    def isconnected(self):
        return self.cn in self.players
    
    def get_player(self, pn=-1):
        if pn == -1:
            pn = self.cn

        if pn in self.players:
            return self.players[pn]
        else:
            raise InvalidPlayerNumberReference(pn)
    