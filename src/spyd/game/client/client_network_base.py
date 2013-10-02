import contextlib

from cube2common.cube_data_stream import CubeDataStream
from spyd.utils.ping_buffer import PingBuffer


class ClientNetworkBase(object):
    def __init__(self, identifier, protocol_wrapper, host, port):
        self.identifier = identifier
        self.protocol_wrapper = protocol_wrapper
        self.host = host
        self.port = port
        
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
        wait = False
        if message is not None:
            wait = True
            self.send_server_message(message)
            self.flush()
        self.protocol_wrapper.disconnect(disconnect_type, wait=wait)
        
    def flush(self):
        self.protocol_wrapper.flush()
