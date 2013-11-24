from twisted.internet import reactor, defer

import spyd.game.client.message_handlers  # @UnusedImport
from cube2common.constants import disconnect_types, MAXNAMELEN, privileges
from spyd.game.player.player import Player
from spyd.game.room.exceptions import RoomEntryFailure
from spyd.game.server_message_formatter import error, smf, info, denied, state_error, usage_error
from spyd.protocol import swh
from spyd.utils.filtertext import filtertext
from spyd.utils.ping_buffer import PingBuffer
import contextlib
from cube2common.cube_data_stream import CubeDataStream
from spyd.game.client.exceptions import InvalidPlayerNumberReference, InsufficientPermissions, StateError, UsageError, GenericError
from spyd.registry_manager import RegistryManager
from spyd.utils.constrain import ConstraintViolation
import traceback
from spyd.game.client.room_group_provider import RoomGroupProvider


class Client(object):
    '''
    Handles the per client networking, and distributes the messages out to the players (main, bots).
    '''
    def __init__(self, protocol, clientnum, room, auth_world_view, permission_resolver, event_subscription_fulfiller, servinfo_domain=""):

        self.cn = clientnum
        self.room = room
        self.players = {}
        self.connection_sequence_complete = False

        self.protocol_wrapper = protocol
        self.host = protocol.transport.host
        self.port = protocol.transport.port

        self.ping_buffer = PingBuffer()

        self._ignored_preconnect_message_types = ("N_POS", "N_PING")
        self._allowed_preconnect_message_types = ("N_CONNECT", "N_AUTHANS")
        self._ignore_client_messages = False

        self._message_handlers = {}
        for registered_message_handler in RegistryManager.get_registrations('client_message_handler'):
            message_handler = registered_message_handler.registered_object
            message_type = message_handler.message_type
            self._message_handlers[message_type] = message_handler

        self.auth_world_view = auth_world_view
        self.auth_deferred = None

        self._permission_resolver = permission_resolver
        self._group_name_providers = []

        self._group_name_providers.append(RoomGroupProvider(self))
        
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

        for player in self.players.itervalues():
            reactor.callLater(60, self._cleanup_player, player)

    def _cleanup_player(self, player):
        player.cleanup()

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
        self.players[self.cn] = player
        
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
        player = self.players[self.cn]
        
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
        return self.cn in self.players and self.connection_sequence_complete

    @property
    def uuid(self):
        return self.get_player().uuid

    def get_player(self, pn=-1):
        if pn == -1:
            pn = self.cn

        if pn in self.players:
            return self.players[pn]
        else:
            raise InvalidPlayerNumberReference(pn)

    def send(self, channel, data, reliable):
        if type(data) != str:
            data = str(data)
        self.protocol_wrapper.send(channel, data, reliable)

    @contextlib.contextmanager
    def sendbuffer(self, channel, reliable):
        cds = CubeDataStream()
        yield cds
        self.send(channel, cds, reliable)

    def disconnect(self, disconnect_type, message=None):
        self.protocol_wrapper.disconnect_with_message(disconnect_type, message, 3.0)

    def get_enet_peer(self):
        return self.protocol_wrapper.transport._enet_peer

    def auth(self, authdomain, authname):
        if self.auth_deferred is not None:
            self.send_server_message(error("You already have a pending auth request wait for the previous one to complete."))
            return defer.fail(None)

        self.auth_deferred = defer.Deferred()

        deferred = self.auth_world_view.try_authenticate(authdomain, authname)

        deferred.addCallback(self.on_auth_challenge)
        deferred.addErrback(self.on_auth_failure)

        return self.auth_deferred

    def answer_auth_challenge(self, authdomain, authid, answer):
        if self.auth_deferred is None:
            return

        deferred = self.auth_world_view.answer_challenge(authdomain, authid, answer)

        deferred.addCallback(self.on_auth_success)
        deferred.addErrback(self.on_auth_failure)

    def on_auth_challenge(self, auth_challenge):
        auth_id = auth_challenge.auth_id
        auth_domain = auth_challenge.auth_domain
        challenge = auth_challenge.challenge

        with self.sendbuffer(1, True) as cds:
            swh.put_authchall(cds, auth_domain, auth_id, challenge)

    def on_auth_failure(self, deferred_exception):
        self.send_server_message(error(deferred_exception.value.message))
        self.auth_deferred.errback(deferred_exception)
        self.auth_deferred = None

    def on_auth_success(self, auth_success):
        if auth_success is not None:
            self.add_group_name_provider(auth_success.group_provider)

            if auth_success.room_message is not None and self.connection_sequence_complete:
                auth_success.room_message_kwargs['client'] = self
                self.room._broadcaster.server_message(info(auth_success.room_message, **auth_success.room_message_kwargs))

        self.auth_deferred.callback(auth_success)
        self.auth_deferred = None

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
                        return
                else:
                    print "Client received unhandled message type:", message_type, message
        except:
            traceback.print_exc()
            self.disconnect(disconnect_types.DISC_MSGERR)
            self._ignore_client_messages = True

    @property
    def privilege(self):
        group_names = self.get_group_names()
        if 'local.room.admin' in group_names:
            return privileges.PRIV_ADMIN
        if 'local.room.auth' in group_names:
            return privileges.PRIV_AUTH
        if 'local.room.master' in group_names:
            return privileges.PRIV_MASTER
        return privileges.PRIV_NONE

    def add_group_name_provider(self, group_name_provider):
        self._group_name_providers.append(group_name_provider)

    def get_group_names(self):
        group_names = set()
        for group_name_provider in self._group_name_providers:
            group_names.update(group_name_provider.get_group_names())
        return group_names

    def allowed(self, functionality):
        group_names = self.get_group_names()
        return self._permission_resolver.groups_allow(group_names, functionality)
