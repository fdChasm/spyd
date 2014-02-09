import time

from twisted.internet import reactor

from spyd.game.server_message_formatter import smf
from spyd.utils.listjoin import listjoin


class NoOpReadyUpController(object):
    def __init__(self, room):
        room.resume()

    def on_crc(self, player, crc):
        pass

    def on_client_spectated(self, client):
        pass

    def on_client_leave(self, client):
        pass

    def on_request_spawn(self, client):
        pass

class MapLoadReadyUpController(object):
    def __init__(self, room, timeout_seconds):
        self.room = room

        if self.room.player_count > 1:
            self.room.set_resuming_state()
            self.wait_clients = set(room.clients)
            self.use_timeout = timeout_seconds is not None
            if self.use_timeout:
                self.timeout = time.time() + timeout_seconds
            self.changed = True
            self.done = False

            reactor.callLater(2, self._check_update)
        else:
            self.room.resume()
            self.wait_clients = set()
            self.changed = False
            self.done = True

    def _check_update(self):
        if self.use_timeout and time.time() > self.timeout:
            player_names = map(lambda c: c.get_player().__format__(None), self.wait_clients)
            player_name_str = listjoin(player_names)
            self.room.server_message(smf.format("Waiting for {player_name_str} to load the map took too long. Starting without them.", player_name_str=player_name_str))

            self.wait_clients.clear()
            self.room.resume()

        if len(self.wait_clients) and self.changed:
            self.changed = False
            player_names = map(lambda c: c.get_player().__format__(None), self.wait_clients)
            player_name_str = listjoin(player_names)
            self.room.server_message(smf.format("Waiting for {player_name_str} to load the map.", player_name_str=player_name_str))

        if len(self.wait_clients):
            reactor.callLater(2, self._check_update)

    def _check_client(self, client):
        if client in self.wait_clients:
            self.changed = True
            self.wait_clients.discard(client)
        if not len(self.wait_clients) and not self.done:
            self.done = True
            self.room.resume()

    def on_crc(self, client, crc):
        self._check_client(client)

    def on_client_spectated(self, client):
        self._check_client(client)

    def on_client_leave(self, client):
        self._check_client(client)

    def on_request_spawn(self, client):
        pass

class ReadyUpControllerFactory(object):
    def __init__(self, config):
        self.config = config
        self.type = config.get('type', 'no_op')

    def make_ready_up_controller(self, room):
        if self.type == 'no_op':
            return NoOpReadyUpController(room)
        elif self.type == 'map_load':
            timeout_seconds = self.config.get('timeout', 5)
            return MapLoadReadyUpController(room, timeout_seconds)
