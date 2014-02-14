import contextlib
import traceback

from twisted.internet import reactor

from cube2common.constants import disconnect_types, MAXNAMELEN
from cube2protocol.cube_data_stream import CubeDataStream
from spyd.game.client.client_auth_state import ClientAuthState
from spyd.game.client.client_permissions import ClientPermissions
from spyd.game.client.client_player_collection import ClientPlayerCollection
from spyd.game.client.exceptions import InsufficientPermissions, StateError, UsageError, GenericError
from spyd.game.client.message_handlers import get_message_handlers
from spyd.game.client.room_group_provider import RoomGroupProvider
from spyd.game.player.player import Player
from spyd.game.room.exceptions import RoomEntryFailure
from spyd.game.server_message_formatter import error, smf, denied, state_error, usage_error
from spyd.protocol import swh
from spyd.utils.constrain import ConstraintViolation
from spyd.utils.filtertext import filtertext
from spyd.utils.ping_buffer import PingBuffer
import time
from twisted.python.failure import Failure


class Client(object):
    '''
    Handles the per client networking, and distributes the messages out to the players (main, bots).
    '''
    def __init__(self, protocol, clientnum_handle, room, auth_world_view, permission_resolver, event_subscription_fulfiller, servinfo_domain=""):

        self.cn_handle = clientnum_handle
        self.cn = clientnum_handle.cn
        self.room = room
        self.connection_sequence_complete = False

        self._client_player_collection = ClientPlayerCollection(self.cn)

        self.protocol_wrapper = protocol
        self.host = protocol.transport.host
        self.port = protocol.transport.port

        self.ping_buffer = PingBuffer()

        self.connect_time = int(time.time())

        self._ignored_preconnect_message_types = ("N_POS", "N_PING")
        self._allowed_preconnect_message_types = ("N_CONNECT", "N_AUTHANS")
        self._ignore_client_messages = False

        self._message_handlers = get_message_handlers()

        self._client_auth_state = ClientAuthState(self, auth_world_view)

        self._client_permissions = ClientPermissions(permission_resolver)

        self.add_group_name_provider(RoomGroupProvider(self))

        self.event_subscription_fulfiller = event_subscription_fulfiller

        self._servinfo_domain = servinfo_domain

        self.command_context = {}

    def __format__(self, format_spec):
        player = self.get_player()

        if player.shares_name or player.isai:
            fmt = "{name#player.name} {pn#player.pn}"
        else:
            fmt = "{name#player.name}"

        return smf.format(fmt, player=player)

    def connected(self):
        print "connect:", self.host
        with self.sendbuffer(1, True) as cds:
            swh.put_servinfo(cds, self, haspwd=False, description="", domain=self._servinfo_domain)

        self.connect_timeout_deferred = reactor.callLater(1, self.connect_timeout)

    def disconnected(self):
        print "disconnect:", self.host
        if self.is_connected:
            self.room.client_leave(self)
            self.event_subscription_fulfiller.publish('spyd.game.player.disconnect', {'player': self.uuid, 'room': self.room.name})

        self.cn_handle.release()
        self._client_player_collection.cleanup_players()

    def connect_timeout(self):
        '''Disconnect client because it didn't send N_CONNECT soon enough.'''
        self.disconnect(disconnect_types.DISC_NONE, message=error("Hey What's up, you didn't send an N_CONNECT message!"))

    def connect_received(self, message):
        '''Create the main player instance for this client and join room.'''
        if not self.connect_timeout_deferred.called:
            self.connect_timeout_deferred.cancel()

        name = filtertext(message['name'], False, MAXNAMELEN)
        playermodel = message['playermodel']
        player = Player(self, self.cn, name, playermodel)
        self.add_player(player)

        pwdhash = message['pwdhash']
        authdomain = message['authdomain']
        authname = message['authname']

        if len(authname) > 0:
            deferred = self.auth(authdomain, authname)

            deferred.addCallback(self.connection_auth_finished, pwdhash)
            deferred.addErrback(lambda e: self.connection_auth_finished(None, pwdhash))
        else:
            self.connection_auth_finished(None, pwdhash)

    def connection_auth_finished(self, authentication, pwdhash):
        player = self.get_player()

        try:
            room_entry_context = self.room.get_entry_context(self, player)
        except RoomEntryFailure as e:
            return self.disconnect(e.disconnect_type, e.message)

        self.room.client_enter(room_entry_context)

        self.connection_sequence_complete = True

        self.event_subscription_fulfiller.publish('spyd.game.player.connect', {'player': self.uuid, 'room': self.room.name})

    def send_server_message(self, message):
        with self.sendbuffer(1, True) as cds:
            swh.put_servmsg(cds, message)

    @property
    def is_connected(self):
        return self.has_pn() and self.connection_sequence_complete

    @property
    def uuid(self):
        return self.get_player().uuid

    @property
    def ping(self):
        return self.ping_buffer.avg()

    @property
    def time_online(self):
        return int(time.time()) - self.connect_time

    def has_pn(self, pn=-1):
        return self._client_player_collection.has_pn(pn=pn)

    def get_player(self, pn=-1):
        return self._client_player_collection.get_player(pn=pn)

    def add_player(self, player):
        self._client_player_collection.add_player(player)

    def player_iter(self):
        return self._client_player_collection.player_iter()

    def send(self, channel, data, reliable, no_allocate=False):
        if type(data) == memoryview:
            data = data.tobytes()
        elif type(data) == CubeDataStream:
            data = memoryview(data.data).tobytes()
        elif type(data) != str:
            data = str(data)
        self.protocol_wrapper.send(channel, data, reliable, no_allocate)

    @contextlib.contextmanager
    def sendbuffer(self, channel, reliable):
        cds = CubeDataStream()
        yield cds
        self.send(channel, cds, reliable)

    def disconnect(self, disconnect_type, message=None, timeout=3.0):
        self.protocol_wrapper.disconnect_with_message(disconnect_type, message, timeout)

    def auth(self, authdomain, authname):
        return self._client_auth_state.auth(authdomain, authname)

    def answer_auth_challenge(self, authdomain, authid, answer):
        return self._client_auth_state.answer_auth_challenge(authdomain, authid, answer)

    def handle_exception(self, e):
        if isinstance(e, Failure):
            e = e.value

        try:
            raise e
        except InsufficientPermissions as e:
            self.send_server_message(denied(e.message))
        except StateError as e:
            self.send_server_message(state_error(e.message))
        except UsageError as e:
            self.send_server_message(usage_error(e.message))
        except GenericError as e:
            self.send_server_message(error(e.message))
        except ConstraintViolation as e:
            print "Disconnecting client {} due to constraint violation {}.".format(self.host, e.constraint_name)
            self.disconnect(disconnect_types.DISC_MSGERR)

    def _message_received(self, message_type, message):
        if self._ignore_client_messages: return
        try:
            if (not self.is_connected) and (message_type in self._ignored_preconnect_message_types):
                pass
            elif (not self.is_connected) and (message_type not in self._allowed_preconnect_message_types):
                print message_type
                self.disconnect(disconnect_types.DISC_MSGERR)
                return
            else:
                if message_type in self._message_handlers:
                    handler = self._message_handlers[message_type]
                    try:
                        handler.handle(self, self.room, message)
                    except Exception as e:
                        self.handle_exception(e)
                else:
                    print "Client received unhandled message type:", message_type, message
        except ConstraintViolation as e:
            pass  # Plenty of information already printed.
        except:
            traceback.print_exc()
            self.disconnect(disconnect_types.DISC_MSGERR)
            self._ignore_client_messages = True

    @property
    def privilege(self):
        return self._client_permissions.privilege

    def add_group_name_provider(self, group_name_provider):
        self._client_permissions.add_group_name_provider(group_name_provider)

    def allowed(self, functionality):
        return self._client_permissions.allowed(functionality)
