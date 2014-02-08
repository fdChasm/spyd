from twisted.application import service
from twisted.internet import reactor

from spyd.server.lan_info.lan_info_protocol import LanInfoProtocol
from spyd.server.lan_info.lan_info_responder import LanInfoResponder


class LanInfoService(service.Service):
    def __init__(self, lan_findable, ext_info_config):
        self.rooms_ports = {}
        self.ext_info_config = ext_info_config
        self.broadcast_listener = None
        if lan_findable:
            self.broadcast_listener = LanInfoProtocol(multicast=True, ext_info_enabled=self.ext_info_config['enabled'])

        self._listeners = []

    def startService(self):
        for room, (interface, port) in self.rooms_ports.iteritems():
            lan_info_protocol = LanInfoProtocol(multicast=False, ext_info_enabled=self.ext_info_config['enabled'])

            lan_info_responder = LanInfoResponder(lan_info_protocol, room, self.ext_info_config)
            lan_info_protocol.add_responder(lan_info_responder)

            if self.broadcast_listener is not None:
                self.broadcast_listener.add_responder(lan_info_responder)

            listener = reactor.listenUDP(port, lan_info_protocol, interface=interface)
            self._listeners.append(listener)

        if self.broadcast_listener is not None:
            listener = reactor.listenMulticast(28784, self.broadcast_listener, interface="0.0.0.0", listenMultiple=True)
            self._listeners.append(listener)

        service.Service.startService(self)

    def stopService(self):
        for listener in self._listeners:
            listener.stopListening()
        service.Service.stopService(self)

    def add_lan_info_for_room(self, room, interface, port):
        self.rooms_ports[room] = (interface, port + 1)
