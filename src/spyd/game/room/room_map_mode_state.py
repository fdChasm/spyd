from spyd.game.client.exceptions import GenericError
from spyd.game.gamemode import gamemodes
from spyd.game.map.map_rotation import MapRotation
from twisted.internet import defer


class RoomMapModeState(object):
    def __init__(self, room, map_rotation=None, map_meta_data_accessor=None):
        self.room = room
        self._map_name = ""
        self._gamemode = None
        self._map_meta_data_accessor = map_meta_data_accessor
        self._map_rotation = map_rotation or MapRotation.from_test_data()
        self._initialized = False

    @property
    def initialized(self):
        return self._initialized

    @property
    def map_name(self):
        if self._gamemode is None:
            map_name, _ = self._map_rotation.next_map_mode(peek=True)
            return map_name
        return self._map_name

    @property
    def gamemode(self):
        return self._gamemode

    @property
    def mode_num(self):
        if self._gamemode is None:
            _, mode_name = self._map_rotation.next_map_mode(peek=True)
            return gamemodes[mode_name].clientmodenum
        return self._gamemode.clientmodenum

    @property
    def mode_name(self):
        if self._gamemode is None:
            _, mode_name = self._map_rotation.next_map_mode(peek=True)
            return gamemodes[mode_name].clientmodename
        return self._gamemode.clientmodename

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
        self.room._new_map_mode_initialize()

        defer.returnValue(map_meta_data)
