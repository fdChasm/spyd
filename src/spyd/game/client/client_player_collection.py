from twisted.internet import reactor

from spyd.game.client.exceptions import InvalidPlayerNumberReference


class ClientPlayerCollection(object):
    def __init__(self, cn):
        self.cn = cn
        self.players = {}

    def has_pn(self, pn=-1):
        if pn == -1:
            pn = self.cn

        return pn in self.players

    def get_player(self, pn=-1):
        if pn == -1:
            pn = self.cn

        if pn in self.players:
            return self.players[pn]
        else:
            raise InvalidPlayerNumberReference(pn)

    def add_player(self, player):
        self.players[player.pn] = player

    def cleanup_players(self):
        for player in self.players.itervalues():
            reactor.callLater(60, self._cleanup_player, player)

    def _cleanup_player(self, player):
        player.cleanup()

    def player_iter(self):
        return self.players.itervalues()
