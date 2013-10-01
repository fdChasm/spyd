from twisted.internet.protocol import DatagramProtocol
from cube2common.read_cube_data_stream import ReadCubeDataStream

class LanInfoProtocol(DatagramProtocol):
    def __init__(self):
        self.lan_info_responders = []
        
    def startProtocol(self):
        self.transport.setTTL(255)

    def add_responder(self, lan_info_responder):
        self.lan_info_responders.append(lan_info_responder)

    def datagramReceived(self, data, address):
        rcds = ReadCubeDataStream(data)
        millis = rcds.getint()
        if not millis == 0:
            for lan_info_responder in self.lan_info_responders:
                lan_info_responder.info_request(address, millis)

    def send(self, data, address):
        self.transport.write(data, address)
