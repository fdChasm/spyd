from twisted.internet import reactor

from cube2common.constants import disconnect_types, MAXNAMELEN
from spyd.game.client.client_authable_base import ClientAuthableBase
from spyd.game.client.client_base import ClientBase
from spyd.game.client.client_message_handling_base import ClientMessageHandlingBase
from spyd.game.client.client_network_base import ClientNetworkBase
from spyd.game.player.player import Player
from spyd.game.room.exceptions import RoomEntryFailure
from spyd.game.server_message_formatter import error, smf
from spyd.protocol import swh
from spyd.utils.filtertext import filtertext
from spyd.game.client.client_permission_base import ClientPermissionBase


class Client(ClientBase, ClientNetworkBase, ClientAuthableBase, ClientMessageHandlingBase, ClientPermissionBase):
    '''
    Handles the per client networking, and distributes the messages out to the players (main, bots).
    '''
    def __init__(self, protocol, clientnum, room, auth_world_view, permission_resolver):
        ClientBase.__init__(self, clientnum, room)
        ClientNetworkBase.__init__(self, protocol)
        ClientAuthableBase.__init__(self, auth_world_view)
        ClientPermissionBase.__init__(self, permission_resolver)
        
        self.command_context = {}
        
        self.is_connected = False
        
    def __format__(self, format_spec):
        player = self.get_player()
        
        if player.shares_name or player.isai:
            fmt = "{name#player.name} {pn#player.pn}"
        else:
            fmt = "{name#player.name}"
            
        return smf.format(fmt, player=player)
    
    def connected(self):
        with self.sendbuffer(1, True) as cds:
            swh.put_servinfo(cds, self, haspwd=False, description="", domain="")
            
        self.connect_timeout_deferred = reactor.callLater(1, self.connect_timeout)

    def disconnected(self):
        if self.is_connected:
            self.room.client_leave(self)

    def connect_timeout(self):
        '''Disconnect client because it didn't send N_CONNECT soon enough.'''
        self.disconnect(disconnect_types.DISC_NONE, message=error("Hey What's up, you didn't send an N_CONNECT message!"))

    def connect_received(self, message):
        '''Create the main player instance for this client and join room.'''
        if not self.connect_timeout_deferred.called:
            self.connect_timeout_deferred.cancel()
        
        name = filtertext(message['name'], False, MAXNAMELEN)
        playermodel = message['playermodel']
        player = Player(self, self.cn, name, playermodel)
        self.players[self.cn] = player
        
        pwdhash = message['pwdhash']
        authdomain = message['authdomain']
        authname = message['authname']
        
        if len(authname) > 0:
            deferred = self.auth(authdomain, authname)
            
            deferred.addCallback(self.connection_auth_finished, pwdhash)
            deferred.addErrback(lambda e: self.connection_auth_finished(None, pwdhash))
        else:
            self.connection_auth_finished(None, pwdhash)
        
    def connection_auth_finished(self, authentication, pwdhash):
        player = self.players[self.cn]
        
        try:
            room_entry_context = self.room.get_entry_context(self, player)
        except RoomEntryFailure as e:
            return self.disconnect(e.disconnect_type, e.message)
        
        self.is_connected = True
        self.room.client_enter(room_entry_context)

    def send_server_message(self, message):
        with self.sendbuffer(1, True) as cds:
            swh.put_servmsg(cds, message)
