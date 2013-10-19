from twisted.protocols.basic import NetstringReceiver

from spyd.registry_manager import register


@register('gep_transport', 'netstring')
class NetstringProtocol(NetstringReceiver):
    def __init__(self, packing):
        self._packing = packing

    def stringReceived(self, data):
        message = self._packing.unpack(data)
        self.controller.receive(message)

    def send(self, message):
        data = self._packing.pack(message)
        self.sendString(data)
        
    def disconnect(self):
        self.transport.loseConnection()
