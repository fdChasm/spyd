from cube2protocol.cube_data_stream import CubeDataStream
from spyd.protocol import swh


class LanInfoResponder(object):
    def __init__(self, lan_info_protocol, room):
        self.lan_info_protocol = lan_info_protocol
        self.room = room
        
    def info_request(self, address, millis):
        cds = CubeDataStream()
        cds.putint(millis)

        swh.put_info_reply(
            cds,
            self.room.lan_info_name,
            self.room.player_count,
            self.room.maxplayers,
            self.room.mode_num,
            self.room.map_name,
            self.room.timeleft,
            self.room.mastermask,
            self.room.is_paused,
            100)

        self.respond(str(cds), address)
        
    def respond(self, data, address):
        self.lan_info_protocol.send(data, address)
