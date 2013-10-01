from sauerpyd.protocol import swh
from cube2common.cube_data_stream import CubeDataStream

class LanInfoResponder(object):
    def __init__(self, lan_info_protocol, room):
        self.lan_info_protocol = lan_info_protocol
        self.room = room
        
    def info_request(self, address, millis):
        cds = CubeDataStream()
        cds.putint(millis)
        #TODO: Get the data from the actual room once the interface for a room is finalized.
        swh.put_info_reply(cds, "Server Name", 12, 16, 12, "forge", 600, 2, 0, 100)
        self.respond(str(cds), address)
        
    def respond(self, data, address):
        self.lan_info_protocol.send(data, address)
