from cube2common.constants import message_types
from cube2common.read_cube_data_stream import ReadCubeDataStream
from spyd.protocol.server_read_stream_protocol import sauerbraten_stream_spec


class MessageProcessor(object):
    def process(self, channel, data):
        if len(data) == 0: return []
        
        if channel == 0:
            messages = self._parse_channel_0_data(data)
        elif channel == 1:
            messages = sauerbraten_stream_spec.read(data, {'aiclientnum':-1})
        
        return messages
        
    def _parse_channel_0_data(self, data):
        cds = ReadCubeDataStream(data)
        message_type = cds.getint()

        if message_type == message_types.N_POS:
            cn = cds.getuint()

            cds.getbyte()

            flags = cds.getuint()

            v = [0, 0, 0]
            for k in range(3):
                n = cds.getbyte()
                n |= cds.getbyte() << 8
                if flags & (1 << k):
                    n |= cds.getbyte() << 16
                    if n & 0x800000:
                        n |= -1 << 24
                v[k] = n

            cds.read(3)

            mag = cds.getbyte()
            if flags & (1 << 3):
                mag |= cds.getbyte() << 8

            dir = cds.getbyte() | (cds.getbyte() << 8)  # @ReservedAssignment

            message = ('N_POS', {'clientnum': cn, 'position': v, 'raw_position': data})
            
        elif message_type == message_types.N_JUMPPAD:
            cn = cds.getint()
            jumppad = cds.getint()
            
            message = ('N_JUMPPAD', {'aiclientnum': cn, 'jumppad': jumppad})

        elif message_type == message_types.N_TELEPORT:
            cn = cds.getint()
            teleport = cds.getint()
            teledest = cds.getint()
            
            message = ('N_TELEPORT', {'aiclientnum': cn, 'teleport': teleport, 'teledest': teledest})
            
        return [message]
            