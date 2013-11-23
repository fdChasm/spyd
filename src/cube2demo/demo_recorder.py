import gzip
import struct

from cube2common.constants import PROTOCOL_VERSION
from cube2common.cube_data_stream import CubeDataStream
from cube2demo.constants import DEMO_MAGIC, DEMO_VERSION


class DemoRecorder(object):
    buffer_class = CubeDataStream

    def __init__(self):
        self.clear()

    def clear(self):
        self._data = bytearray()

    def record(self, millis, channel, data):
        # millis(int), channel(int), length(int), data(length#bytes)
        length = len(data)
        self._data.extend(struct.pack('iii', millis, channel, length))
        self._data.extend(data)

    def write(self, demo_filename):
        with gzip.open(demo_filename, 'wb') as f:
            f.write(struct.pack("16sii", DEMO_MAGIC, DEMO_VERSION, PROTOCOL_VERSION))
            f.write(str(self._data))
