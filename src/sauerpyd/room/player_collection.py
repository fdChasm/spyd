class PlayerCollection(object):
    def __init__(self):
        #pn: player
        self._players = {}
        
    def add(self, player):
        self._players[player.pn] = player
        
    def remove(self, player):
        del self._players[player.pn]
    
    def to_list(self):
        return self._players.values()
    
    def to_iterator(self):
        return self._players.itervalues()
    
    def by_pn(self, pn):
        return self._players[pn]
    
    def is_name_duplicate(self, name):
        name_count = 0
        for player in self._players.itervalues():
            if player.name == name:
                name_count += 1
                if name_count > 1:
                    return True
        return False