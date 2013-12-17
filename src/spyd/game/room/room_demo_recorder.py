import contextlib

from spyd.protocol import swh


class RoomDemoRecorder(object):
    def __init__(self, room, demo_recorder):
        self._room = room
        self._demo_recorder = demo_recorder
        self.clear()

    def write(self, demo_filename):
        self._demo_recorder.write(demo_filename)

    def clear(self):
        self._demo_recorder.clear()

    def record(self, channel, data):
        self._demo_recorder.record(self._room.gamemillis, channel, data)

    @contextlib.contextmanager
    def demobuffer(self, channel):
        cds = self._demo_recorder.buffer_class()
        yield cds
        self.record(channel, str(cds))

    def initialize_demo_recording(self):
        self._demo_recorder.clear()
        with self.demobuffer(1) as cds:
            swh.put_welcome(cds)

            swh.put_currentmaster(cds, self._room.mastermode, self._room._clients.to_iterator())

            swh.put_mapchange(cds, self._room._map_mode_state.map_name, self._room._map_mode_state.mode_num, hasitems=False)

            if self._room.gamemode.timed and self._room.timeleft is not None:
                swh.put_timeup(cds, self._room.timeleft)

            if self._room.is_paused:
                swh.put_pausegame(cds, 1)

            existing_players = list(self._room.players)
            swh.put_initclients(cds, existing_players)
            swh.put_resume(cds, existing_players)
