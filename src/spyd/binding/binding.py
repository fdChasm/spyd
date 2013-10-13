import enet
import logging

handled_enet_events = (enet.EVENT_TYPE_CONNECT, enet.EVENT_TYPE_DISCONNECT, enet.EVENT_TYPE_RECEIVE)

class Binding(object):
    def __init__(self, corresponder, interface, port, maxclients, maxup, maxdown, channels, timeout):
        self.logger = logging.getLogger(__name__)
        self.corresponder = corresponder
        self.interface = interface
        self.port = port
        self.maxclients = maxclients
        self.maxup = maxup
        self.maxdown = maxdown
        self.channels = channels
        self.timeout = timeout
        
        self.logger.info("binding server to {}:{}".format(self.interface, self.port, timeout))
        
        self.address = enet.Address(self.interface, self.port)
        self.host = enet.Host(self.address, self.maxclients, self.channels, self.maxdown, self.maxup)
        
        #identifier: EnetPeer
        self.peers = {}
        
        #identifier: disconnect_type, rid
        self.pending_disconnect = {}
        '''
        When clients are disconnected we send the controller a disconnected message right away and begin ignoring messages from that enet peer.
        Sometimes we need to ensure a message reaches the first so we wait until a flush occurs before actually disconnecting the enet peer.
        '''
            
    def run(self):
        while True:
            self._service_host()
            self._process_cmds()

    def flush(self):
        self.host.flush()

    def _service_host(self):
        event = self.host.service(self.timeout)
        
        if not event.type in handled_enet_events: return
        
        identifier = self.port, event.peer.incomingSessionID, event.peer.incomingPeerID

        if event.type == enet.EVENT_TYPE_CONNECT:
            self.peers[identifier] = event.peer
            message = {'type':  'connect', 
                       'ident': identifier, 
                       'host':  event.peer.address.host, 
                       'port':  event.peer.address.port,
                       'binding': {
                           'port':      self.port,
                           'interface': self.interface,
                       }}
            self.corresponder.send(message)

        elif event.type == enet.EVENT_TYPE_DISCONNECT:
            if identifier in self.peers:
                del self.peers[identifier]
                self.corresponder.send({'type': 'disconnect', 'ident': identifier})

        elif event.type == enet.EVENT_TYPE_RECEIVE:
            if identifier in self.pending_disconnect:
                disconnect_type, rid = self.pending_disconnect.pop(identifier)
                result = event.peer.disconnect(disconnect_type)
                self.corresponder.send({'type': 'response', 'rid': rid, 'result': result})
            else:
                self.corresponder.send({'type': 'receive', 'ident': identifier, 'data': event.packet.data, 'channel': event.channelID})
        
    def _process_cmds(self):
        commands = self.corresponder.receive(0.0)
        for command in commands:
            handler_name = "_on_cmd_{}".format(command['type'])
            handler = getattr(self, handler_name)
            handler(command)
            
    def _on_cmd_flush(self, command):
        self.flush()
        self.corresponder.send({'type': 'response', 'rid': command['rid'], 'result': 0})
    
    def _on_cmd_send(self, command):
        identifier = command['ident']
        
        peer = self.peers.get(identifier, None)
        if peer is None: return
        
        flags = enet.PACKET_FLAG_RELIABLE if command['reliable'] else 0

        packet = enet.Packet(command['data'], flags)
        result = peer.send(command['channel'], packet)
        
        self.corresponder.send({'type': 'response', 'rid': command['rid'], 'result': result})
        
    def _on_cmd_disconnect(self, command):
        identifier = command['ident']
        
        peer = self.peers.get(identifier, None)
        if peer is None: return
        
        disconnect_type = command['dt']
        wait = command.get('wait', False)
        
        if not wait:
            result = peer.disconnect(disconnect_type)
            self.corresponder.send({'type': 'response', 'rid': command['rid'], 'result': result})
        else:
            self.pending_disconnect[identifier] = (disconnect_type, command['rid'])
