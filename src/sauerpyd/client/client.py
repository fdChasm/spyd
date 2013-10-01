from twisted.internet import reactor

from cube2common.constants import disconnect_types, MAXNAMELEN
from sauerpyd.client.client_authable_base import ClientAuthableBase
from sauerpyd.client.client_base import ClientBase
from sauerpyd.client.client_network_base import ClientNetworkBase
from sauerpyd.player.player import Player
from sauerpyd.protocol import swh
from sauerpyd.server_message_formatter import error
from utils.filtertext import filtertext
from sauerpyd.client.client_message_handling_base import ClientMessageHandlingBase
from sauerpyd.room.exceptions import RoomEntryFailure


class Client(ClientBase, ClientNetworkBase, ClientAuthableBase, ClientMessageHandlingBase):
    '''
    Handles the per client networking, and distributes the messages out to the players (main, bots).
    '''
    def __init__(self, identifier, protocol, host, port, clientnum, room, master_client):
        ClientBase.__init__(self, clientnum, room)
        ClientNetworkBase.__init__(self, identifier, protocol, host, port)
        ClientAuthableBase.__init__(self, master_client)
        
        self.is_connected = False
    
    def connected(self):
        print "Client connected called."
        with self.sendbuffer(1, True) as cds:
            swh.put_servinfo(cds, self, haspwd=False, description="Test Server", domain="")
            
        self.connect_timeout_deferred = reactor.callLater(1, self.connect_timeout)

    def disconnected(self):
        if self.is_connected:
            self.room.client_leave(self)
        print "Client disconnected called."

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
            room_entry_context = self.room.get_entry_context(self, player, authentication, pwdhash)
        except RoomEntryFailure as e:
            return self.disconnect(e.disconnect_type, e.message)
        
        self.is_connected = True
        self.room.client_enter(room_entry_context)

    def send_server_message(self, message):
        with self.sendbuffer(1, True) as cds:
            swh.put_servmsg(cds, message)
