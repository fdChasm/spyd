import contextlib

from cube2common.cube_data_stream import CubeDataStream
from spyd.utils.ping_buffer import PingBuffer


class ClientNetworkBase(object):
    def __init__(self, protocol):
        self.protocol_wrapper = protocol
        self.host = protocol.transport.host
        self.port = protocol.transport.port
        
        self.ping_buffer = PingBuffer()
    
    def send(self, channel, data, reliable):
        if type(data) != str:
            data = str(data)
        self.protocol_wrapper.send(channel, data, reliable)
        
    @contextlib.contextmanager
    def sendbuffer(self, channel, reliable):
        cds = CubeDataStream()
        yield cds
        self.send(channel, cds, reliable)
    
    def disconnect(self, disconnect_type, message=None):
        self.protocol_wrapper.disconnect_with_message(disconnect_type, message, 3.0)

    def get_enet_peer(self):
        return self.protocol_wrapper.transport._enet_peer
