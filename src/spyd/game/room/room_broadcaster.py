import contextlib
import traceback

from cube2protocol.cube_data_stream import CubeDataStream
from spyd.protocol import swh


class RoomBroadcaster(object):
    def __init__(self, client_collection, player_collection, demo_recorder):
        self._client_collection = client_collection
        self._player_collection = player_collection
        self._demo_recorder = demo_recorder

    @contextlib.contextmanager
    def broadcastbuffer(self, channel, reliable, *args):
        with self.clientbuffer(channel, reliable, *args) as cds:
            yield cds
            self._demo_recorder.record(channel, str(cds))

    @property
    def clientbuffer(self):
        return self._client_collection.broadcastbuffer

    def resume(self):
        with self.broadcastbuffer(1, True) as cds:
            swh.put_pausegame(cds, 0)

    def pause(self):
        with self.broadcastbuffer(1, True) as cds:
            swh.put_pausegame(cds, 1)

    def time_left(self, seconds):
        with self.broadcastbuffer(1, True) as cds:
            swh.put_timeup(cds, seconds)

    def intermission(self):
        self.time_left(0)

    def shotfx(self, player, gun, shot_id, from_pos, to_pos):
        with self.broadcastbuffer(1, True, [player]) as cds:
            swh.put_shotfx(cds, player, gun, shot_id, from_pos, to_pos)

    def explodefx(self, player, gun, explode_id):
        with self.broadcastbuffer(1, True, [player]) as cds:
            swh.put_explodefx(cds, player, gun, explode_id)

    def player_died(self, player, killer):
        with self.broadcastbuffer(1, True) as cds:
            swh.put_died(cds, player, killer)

    def player_disconnected(self, player):
        with self.broadcastbuffer(1, True) as cds:
            swh.put_cdis(cds, player)

    def teleport(self, player, teleport, teledest):
        with self.broadcastbuffer(0, True, [player]) as cds:
            swh.put_teleport(cds, player, teleport, teledest)

    def jumppad(self, player, jumppad):
        with self.broadcastbuffer(0, True, [player]) as cds:
            swh.put_jumppad(cds, player, jumppad)

    def server_message(self, message, exclude=()):
        with self.broadcastbuffer(1, True, exclude) as cds:
            swh.put_servmsg(cds, message)

    def client_connected(self, client):
        player = client.get_player()
        with self.broadcastbuffer(1, True, [client]) as cds:
            swh.put_resume(cds, [player])
            swh.put_initclients(cds, [player])
            
    def current_masters(self, mastermode, clients):
        with self.broadcastbuffer(1, True) as cds:
            swh.put_currentmaster(cds, mastermode, clients)
            
    def sound(self, sound):
        for client in self._client_collection.to_iterator():
            with client.sendbuffer(1, True) as cds:
                tm = CubeDataStream()
                swh.put_sound(tm, sound)
                swh.put_clientdata(cds, client, str(tm))

    def flush_messages(self):
        try:
            for client in self._client_collection.to_iterator():

                room_positions = CubeDataStream()
                room_messages = CubeDataStream()

                for player in self._player_collection.to_iterator():
                    if player.client == client: continue
                    player.write_state(room_positions, room_messages)

                if not room_positions.empty():
                    client.send(0, room_positions, True)

                if not room_messages.empty():
                    client.send(1, room_messages, True)

            for player in self._player_collection.to_iterator():
                player.state.clear_flushed_state()
        except:
            traceback.print_exc()
