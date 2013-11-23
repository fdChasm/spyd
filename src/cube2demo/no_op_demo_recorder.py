from cube2common.cube_data_stream import CubeDataStream


class NoOpDemoRecorder(object):
    buffer_class = CubeDataStream

    def __init__(self):
        pass

    def clear(self):
        pass

    def record(self, millis, channel, data):
        pass

    def write(self, demo_filename):
        pass
