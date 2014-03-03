import uuid

from spyd.game.map.team import NullTeam
from spyd.game.player.player_state import PlayerState
from spyd.game.server_message_formatter import smf
from spyd.protocol import swh


class Player(object):

    instances_by_uuid = {}

    def __init__(self, client, playernum, name, playermodel):
        self.client = client
        self._pn = playernum
        self.name = name
        self.playermodel = playermodel
        self._team = NullTeam()
        self._isai = False
        self._uuid = str(uuid.uuid4())

        Player.instances_by_uuid[self.uuid] = self

        self._state = PlayerState()

    @property
    def cn(self):
        return self._pn

    @property
    def pn(self):
        return self._pn

    @property
    def ping(self):
        return self.client.ping

    @property
    def privilege(self):
        if self.isai: return 0
        else: return self.client.privilege

    @property
    def state(self):
        return self._state

    @property
    def isai(self):
        return self._isai

    @property
    def uuid(self):
        return self._uuid

    @property
    def room(self):
        return self.client.room

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, team):
        self._team = team or NullTeam()

    @property
    def team_name(self):
        return self.team.name

    @property
    def shares_name(self):
        return self.room.is_name_duplicate(self.name)

    def __format__(self, format_spec):
        if self.shares_name or self.isai:
            fmt = "{name#player.name} {pn#player.pn}"
        else:
            fmt = "{name#player.name}"

        return smf.format(fmt, player=self)

    def on_respawn(self, lifesequence, gunselect):
        self.state.on_respawn(lifesequence, gunselect)

    def write_state(self, room_positions, room_messages):
        if self.state.position is not None:
            room_positions.write(self.state.position)

        if not self.state.messages.empty():
            swh.put_clientdata(room_messages, self, self.state.messages)

    def cleanup(self):
        Player.instances_by_uuid.pop(self.uuid, None)

    def send(self, channel, data, reliable):
        return self.client.send(channel, data, reliable)

    def send_server_message(self, message):
        self.client.send_server_message(message)

    @property
    def sendbuffer(self):
        return self.client.sendbuffer
