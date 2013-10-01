from twisted.application import service
from twisted.internet import reactor
from server.lan_info.lan_info_protocol import LanInfoProtocol
from server.lan_info.lan_info_responder import LanInfoResponder

class LanInfoService(service.Service):
    def __init__(self, lan_findable):
        self.rooms_ports = {}
        self.broadcast_listener = None
        if lan_findable:
            self.broadcast_listener = LanInfoProtocol()
    
    def startService(self):
        for room, (interface, port) in self.rooms_ports.iteritems():
            lan_info_protocol = LanInfoProtocol()
            
            lan_info_responder = LanInfoResponder(lan_info_protocol, room)
            lan_info_protocol.add_responder(lan_info_responder)
            
            if self.broadcast_listener is not None:
                self.broadcast_listener.add_responder(lan_info_responder)
            
            reactor.listenMulticast(port, lan_info_protocol, interface=interface, listenMultiple=True)
            
        if self.broadcast_listener is not None:
            reactor.listenMulticast(28784, self.broadcast_listener, interface="0.0.0.0", listenMultiple=True)
            
        service.Service.startService(self)
        
    def add_lan_info_for_room(self, room, interface, port):
        self.rooms_ports[room] = (interface, port+1)
