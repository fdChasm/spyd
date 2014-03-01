from twisted.internet import defer

from cube2common.constants import INTERMISSIONLEN
from spyd.game.client.exceptions import GenericError
from spyd.game.gamemode import gamemodes
from spyd.game.map.map_rotation import MapRotation
from spyd.protocol import swh


class RoomMapModeState(object):
    def __init__(self, room, map_rotation=None, map_meta_data_accessor=None, game_clock=None, ready_up_controller_factory=None):
        self.room = room
        self._map_name = ""
        self._gamemode = None
        self._map_meta_data_accessor = map_meta_data_accessor
        self._map_rotation = map_rotation or MapRotation.from_test_data()
        self._game_clock = game_clock
        self._ready_up_controller_factory = ready_up_controller_factory
        self._initialized = False

    @property
    def initialized(self):
        return self._initialized

    @property
    def map_name(self):
        if self.gamemode is None:
            map_name, _ = self._map_rotation.next_map_mode(peek=True)
            return map_name
        return self._map_name

    @property
    def gamemode(self):
        return self._gamemode

    @property
    def mode_num(self):
        if self.gamemode is None:
            _, mode_name = self._map_rotation.next_map_mode(peek=True)
            return gamemodes[mode_name].clientmodenum
        return self.gamemode.clientmodenum

    @property
    def mode_name(self):
        if self.gamemode is None:
            _, mode_name = self._map_rotation.next_map_mode(peek=True)
            return gamemodes[mode_name].clientmodename
        return self.gamemode.clientmodename

    def get_map_names(self):
        return self._map_meta_data_accessor.get_map_names()

    @property
    def rotate_on_first_player(self):
        return self._map_rotation.rotate_on_first_player

    def rotate_map_mode(self):
        map_name, mode_name = self._map_rotation.next_map_mode(peek=False)
        return self.change_map_mode(map_name, mode_name)

    @defer.inlineCallbacks
    def change_map_mode(self, map_name, mode_name):
        if mode_name not in gamemodes:
            raise GenericError("Unsupported game mode.")

        self._map_name = map_name

        map_meta_data = yield self._map_meta_data_accessor.get_map_data(self._map_name)
        map_meta_data = map_meta_data or {}

        self._gamemode = gamemodes[mode_name](room=self.room, map_meta_data=map_meta_data)
        self._initialized = True
        self._new_map_mode_initialize()

        defer.returnValue(map_meta_data)

    def _new_map_mode_initialize(self):
        with self.room.broadcastbuffer(1, True) as cds:
            swh.put_mapchange(cds, self.map_name, self.gamemode.clientmodenum, hasitems=False)

            for player in self.room.players:
                self.gamemode.initialize_player(cds, player)

        if self.gamemode.timed:
            self._game_clock.start(self.gamemode.timeout, INTERMISSIONLEN)
        else:
            self._game_clock.start_untimed()

        self.room.ready_up_controller = self._ready_up_controller_factory.make_ready_up_controller(self.room)

        for player in self.room.players:
            player.state.map_change_reset()
            player.state.respawn()
            self.gamemode.spawn_loadout(player)

        for client in self.room.clients:
            with client.sendbuffer(1, True) as cds:

                if self.gamemode.timed and self.room.timeleft is not None:
                    swh.put_timeup(cds, self.room.timeleft)

                if self.room.is_paused:
                    swh.put_pausegame(cds, 1)

                for player in client.player_iter():
                    if not player.state.is_spectator:
                        swh.put_spawnstate(cds, player)

        self.room._initialize_demo_recording()
