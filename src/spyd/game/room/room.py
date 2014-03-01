import math
import traceback

from twisted.internet import reactor, defer

from cube2common.constants import MAXROOMLEN, MAXSERVERDESCLEN, MAXSERVERLEN, mastermodes, privileges
from cube2demo.no_op_demo_recorder import NoOpDemoRecorder
from spyd.game.awards import display_awards
from spyd.game.client.exceptions import InsufficientPermissions, GenericError
from spyd.game.room.client_collection import ClientCollection
from spyd.game.room.client_event_handlers import get_client_event_handlers
from spyd.game.room.player_collection import PlayerCollection
from spyd.game.room.player_event_handlers import get_player_event_handlers
from spyd.game.room.room_broadcaster import RoomBroadcaster
from spyd.game.room.room_demo_recorder import RoomDemoRecorder
from spyd.game.room.room_entry_context import RoomEntryContext
from spyd.game.room.room_map_mode_state import RoomMapModeState
from spyd.game.server_message_formatter import smf
from spyd.game.timing.game_clock import GameClock
from spyd.permissions.functionality import Functionality
from spyd.protocol import swh
from spyd.server.metrics.execution_timer import ExecutionTimer
from spyd.utils.truncate import truncate
from spyd.utils.value_model import ValueModel


class Room(object):
    '''
    The room serves as the central hub for all players who are in the same game.
    It provides four things;
    * Event handling functions which accept client events
    * Event handling functions which accept player events
    * Accessors to query the state of the room.
    * Setters to modify the state of the room.
    '''
    def __init__(self, ready_up_controller_factory, metrics_service=None, room_name=None, room_manager=None, server_name_model=None, map_rotation=None, map_meta_data_accessor=None, command_executer=None, event_subscription_fulfiller=None, maxplayers=None, show_awards=True, demo_recorder=None):
        self._game_clock = GameClock()
        self._attach_game_clock_event_handlers()

        self._metrics_service = metrics_service

        self.manager = room_manager

        self._server_name_model = server_name_model or ValueModel("123456789ABCD")
        self._name = ValueModel(room_name or "1234567")
        self._server_name_model.observe(self._on_name_changed)
        self._name.observe(self._on_name_changed)

        self._flush_positions_execution_timer = ExecutionTimer(self._metrics_service, 'room.{}.flush_positions'.format(self.name), 1.0)

        self._clients = ClientCollection()
        self._players = PlayerCollection()

        # '123.321.123.111': {client, client, client}
        self._client_ips = {}

        self.command_executer = command_executer
        self.command_context = {}

        self.event_subscription_fulfiller = event_subscription_fulfiller

        self.maxplayers = maxplayers

        self.temporary = False
        self.decommissioned = False

        self.show_awards = show_awards

        self.demo_recorder = RoomDemoRecorder(self, demo_recorder or NoOpDemoRecorder())

        self.mastermask = 0 if self.temporary else -1
        self.mastermode = 0
        self.resume_delay = None

        self.last_destination_room = None

        # Holds the client objects with each level of permissions
        self.masters = set()
        self.auths = set()
        self.admins = set()

        self._client_event_handlers = get_client_event_handlers()
        self._player_event_handlers = get_player_event_handlers()

        self.ready_up_controller = None

        self._map_mode_state = RoomMapModeState(self, map_rotation, map_meta_data_accessor, self._game_clock, ready_up_controller_factory)

        self._broadcaster = RoomBroadcaster(self._clients, self._players, self.demo_recorder)
        reactor.addSystemEventTrigger('before', 'flush_bindings', self._flush_messages)

    ###########################################################################
    #######################        Accessors        ###########################
    ###########################################################################

    def __format__(self, format_spec):
        return smf.format("{room#room.name}", room=self)

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name.value = truncate(value, MAXROOMLEN)

    @property
    def lan_info_name(self):
        server_name = truncate(self._server_name_model.value, MAXSERVERLEN)
        room_title = smf.format("{server_name} #{room.name}", room=self, server_name=server_name)
        return room_title

    def get_entry_context(self, client, player):
        '''
        Returns an object which encapsulates the details about a client request
        to join this room.
        This gives the room an opportunity to raise exceptions before any
        work change actually happen. (for example room being full, or private.)
        '''
        return RoomEntryContext(client)

    @property
    def clients(self):
        return self._clients.to_iterator()

    @property
    def players(self):
        return self._players.to_iterator()

    @property
    def playing_count(self):
        count = 0
        for player in self.players:
            if not player.state.is_spectator:
                count += 1
        return count

    @property
    def player_count(self):
        return self._clients.count

    @property
    def empty(self):
        return self.player_count == 0

    def get_client(self, cn):
        return self._clients.by_cn(cn)

    def get_player(self, pn):
        return self._players.by_pn(pn)

    @property
    def is_paused(self):
        return self._game_clock.is_paused

    @property
    def is_resuming(self):
        return self._game_clock.is_resuming

    @property
    def is_intermission(self):
        return self._game_clock.is_intermission

    @property
    def timeleft(self):
        return int(math.ceil(self._game_clock.timeleft))

    @timeleft.setter
    def timeleft(self, seconds):
        self._game_clock.timeleft = seconds

    @property
    def gamemillis(self):
        return int(self._game_clock.time_elapsed * 1000)

    @property
    def gamemode(self):
        return self._map_mode_state.gamemode

    @property
    def map_name(self):
        return self._map_mode_state.map_name

    @property
    def mode_num(self):
        return self._map_mode_state.mode_num

    @property
    def is_teammode(self):
        return self.gamemode.hasteams

    @property
    def mode_name(self):
        return self._map_mode_state.mode_name

    def get_map_names(self):
        return self._map_mode_state.get_map_names()

    def is_name_duplicate(self, name):
        return self._players.is_name_duplicate(name)

    def contains_client_with_ip(self, client_ip):
        return self._client_ips.has_key(client_ip)

    ###########################################################################
    #######################         Setters         ###########################
    ###########################################################################

    @defer.inlineCallbacks
    def client_enter(self, entry_context):
        if not self._map_mode_state.initialized or self._map_mode_state.rotate_on_first_player and len(self.players) == 0:
            yield self.rotate_map_mode()

        client = entry_context.client
        player = client.get_player()

        player.state.use_game_clock(self._game_clock)

        self._initialize_client(client)
        self._broadcaster.client_connected(client)

        self._clients.add(client)
        self._players.add(player)

        if not client.host in self._client_ips:
            self._client_ips[client.host] = set()
        self._client_ips[client.host].add(client)

        if client in self.admins or client in self.masters or client in self.auths:
            self._update_current_masters()

        self.gamemode.on_player_connected(player)

    def client_leave(self, client):
        self._clients.remove(client)
        for player in client.player_iter():
            self._player_disconnected(player)

        if client in self.masters or client in self.admins:
            self.masters.discard(client)
            self.auths.discard(client)
            self.admins.discard(client)

        clients_with_ip = self._client_ips.get(client.host, set())
        clients_with_ip.discard(client)
        if len(clients_with_ip) == 0:
            del self._client_ips[client.host]

        with client.sendbuffer(1, True) as cds:
            for remaining_client in self._clients.to_iterator():
                swh.put_cdis(cds, remaining_client)

        self.ready_up_controller.on_client_leave(client)

        self.manager.on_room_player_count_changed(self)

    def pause(self):
        self._game_clock.pause()

    def resume(self):
        self._game_clock.resume(self.resume_delay)

    def set_resuming_state(self):
        "Used to set the game clock into the resuming state pending some external event."
        self._game_clock.set_resuming_state()

    def end_match(self):
        self._game_clock.timeleft = 0

    def change_map_mode(self, map_name, mode_name):
        if not self.is_intermission:
            self._finalize_demo_recording()
        self._game_clock.cancel()
        return self._map_mode_state.change_map_mode(map_name, mode_name)

    def rotate_map_mode(self):
        self._game_clock.cancel()
        return self._map_mode_state.rotate_map_mode()

    def set_mastermode(self, mastermode):
        self.mastermode = mastermode
        self._update_current_masters()

    @property
    def broadcastbuffer(self):
        return self._broadcaster.broadcastbuffer

    @property
    def demobuffer(self, channel):
        return self.demo_recorder.demobuffer

    def server_message(self, message, exclude=()):
        self._broadcaster.server_message(message, exclude)

    ###########################################################################
    #######################  Client event handling  ###########################
    ###########################################################################

    def handle_client_event(self, event_name, *args, **kwargs):
        if event_name in self._client_event_handlers:
            event_handler = self._client_event_handlers[event_name]
            event_handler.handle(self, *args, **kwargs)
        else:
            print "Unhandled client event: {} with args: {}, {}".format(event_name, args, kwargs)

    ###########################################################################
    #######################  Player event handling  ###########################
    ###########################################################################

    def handle_player_event(self, event_name, *args, **kwargs):
        if event_name in self._player_event_handlers:
            event_handler = self._player_event_handlers[event_name]
            event_handler.handle(self, *args, **kwargs)
        else:
            print "Unhandled player event: {} with args: {}, {}".format(event_name, args, kwargs)

    ###########################################################################
    #####################  Game clock event handling  #########################
    ###########################################################################

    def _attach_game_clock_event_handlers(self):
        self._game_clock.add_resumed_callback(self._on_game_clock_resumed)
        self._game_clock.add_paused_callback(self._on_game_clock_paused)
        self._game_clock.add_resume_countdown_tick_callback(self._on_game_clock_resume_countdown_tick)
        self._game_clock.add_timeleft_altered_callback(self._on_game_clock_timeleft_altered)
        self._game_clock.add_intermission_started_callback(self._on_game_clock_intermission)
        self._game_clock.add_intermission_ended_callback(self._on_game_clock_intermission_ended)

    def _on_game_clock_resumed(self):
        self._broadcaster.resume()
        if not self.gamemode.initialized:
            self.gamemode.initialize()

    def _on_game_clock_paused(self):
        self._broadcaster.pause()

    def _on_game_clock_resume_countdown_tick(self, seconds):
        self._broadcaster.server_message(smf.format("Resuming in {value#seconds}...", seconds=seconds))

    def _on_game_clock_timeleft_altered(self, seconds):
        self._broadcaster.time_left(int(math.ceil(seconds)))

    def _on_game_clock_intermission(self):
        self._finalize_demo_recording()
        self._broadcaster.intermission()
        if self.show_awards:
            display_awards(self)

    def _on_game_clock_intermission_ended(self):
        self._broadcaster.server_message("Intermission has ended.")
        try:
            self.rotate_map_mode()
        except:
            traceback.print_exc()

    ###########################################################################
    #######################  Other private methods  ###########################
    ###########################################################################

    def _flush_messages(self):
        if not self.decommissioned:
            reactor.callLater(0, reactor.addSystemEventTrigger, 'before', 'flush_bindings', self._flush_messages)
        with self._flush_positions_execution_timer.measure():
            self._broadcaster.flush_messages()

    def _initialize_client_match_data(self, cds, client):
        player = client.get_player()

        swh.put_mapchange(cds, self._map_mode_state.map_name, self._map_mode_state.mode_num, hasitems=False)

        if self.gamemode.timed and self.timeleft is not None:
            swh.put_timeup(cds, self.timeleft)

        if self.is_paused:
            swh.put_pausegame(cds, 1)

        if self.mastermode >= mastermodes.MM_LOCKED:
            player.state.is_spectator = True
            swh.put_spectator(cds, player)

        self.gamemode.initialize_player(cds, player)

        if not player.state.is_spectator and not self.is_intermission:
            player.state.respawn()
            self.gamemode.spawn_loadout(player)
            swh.put_spawnstate(cds, player)

    def _initialize_client(self, client):
        existing_players = list(self.players)

        with client.sendbuffer(1, True) as cds:
            swh.put_welcome(cds)
            self._put_room_title(cds, client)

            possible_privileged_clients = [client] + self._clients.to_list()

            swh.put_currentmaster(cds, self.mastermode, possible_privileged_clients)

            self._initialize_client_match_data(cds, client)

            swh.put_initclients(cds, existing_players)
            swh.put_resume(cds, existing_players)

    def _player_disconnected(self, player):
        self._players.remove(player)
        self._broadcaster.player_disconnected(player)
        self.gamemode.on_player_disconnected(player)

    def _get_room_title(self):
        server_name = truncate(self._server_name_model.value, MAXSERVERLEN)
        room_title = smf.format("{server_name} {room_title#room.name}", room=self, server_name=server_name)
        return room_title

    def _put_room_title(self, cds, client):
        room_title = truncate(self._get_room_title(), MAXSERVERDESCLEN)
        swh.put_servinfo(cds, client, haspwd=False, description=room_title, domain='')

    def _send_room_title(self, client):
        with client.sendbuffer(1, True) as cds:
            self._put_room_title(cds, client)

    def _on_name_changed(self, *args):
        for client in self.clients:
            self._send_room_title(client)

    def _set_player_spectator(self, player, spectate):
        if not spectate and player.state.is_spectator:
            self.gamemode.on_player_unspectate(player)

        elif spectate and not player.state.is_spectator:
            self.gamemode.on_player_spectate(player)

        else:
            print "invalid change"

    set_self_privilege_functionality_tree = {
        'temporary': {
            'claim': {
                privileges.PRIV_MASTER: Functionality("spyd.game.room.temporary.claim_master", "You do not have permission to claim master."),
                privileges.PRIV_AUTH: Functionality("spyd.game.room.temporary.claim_auth", "You do not have permission to claim auth."),
                privileges.PRIV_ADMIN: Functionality("spyd.game.room.temporary.claim_admin", "You do not have permission to claim admin.")
            },
            'relinquish': {
                privileges.PRIV_MASTER: Functionality("spyd.game.room.temporary.relinquish_master", "Cannot relinquish master."),
                privileges.PRIV_AUTH: Functionality("spyd.game.room.temporary.relinquish_auth", "Cannot relinquish auth."),
                privileges.PRIV_ADMIN: Functionality("spyd.game.room.temporary.relinquish_admin", "Cannot relinquish master.")
            }
        },
        'permanent': {
            'claim': {
                privileges.PRIV_MASTER: Functionality("spyd.game.room.permanent.claim_master", "You do not have permission to claim master in permanent rooms."),
                privileges.PRIV_AUTH: Functionality("spyd.game.room.permanent.claim_auth", "You do not have permission to claim auth in permanent rooms."),
                privileges.PRIV_ADMIN: Functionality("spyd.game.room.permanent.claim_admin", "You do not have permission to claim admin in permanent rooms.")
            },
            'relinquish': {
                privileges.PRIV_MASTER: Functionality("spyd.game.room.permanent.relinquish_master", "Cannot relinquish master."),
                privileges.PRIV_AUTH: Functionality("spyd.game.room.permanent.relinquish_auth", "Cannot relinquish auth."),
                privileges.PRIV_ADMIN: Functionality("spyd.game.room.permanent.relinquish_admin", "Cannot relinquish master.")
            }
        }
    }


    def _client_change_privilege(self, client, target, requested_privilege):
        if requested_privilege == privileges.PRIV_NONE:
            self.admins.discard(target)
            self.auths.discard(target)
            self.masters.discard(target)
        elif requested_privilege == privileges.PRIV_MASTER:
            self.masters.add(target)
        elif requested_privilege == privileges.PRIV_AUTH:
            self.auths.add(target)
        elif requested_privilege == privileges.PRIV_ADMIN:
            self.admins.add(target)
        self._update_current_masters()

    def _set_self_privilege(self, client, requested_privilege):
        room_classification = "temporary" if self.temporary else "permanent"

        if requested_privilege > privileges.PRIV_NONE:
            privilege_action = "claim"
            permission_involved = requested_privilege
        else:
            privilege_action = "relinquish"
            permission_involved = client.privilege

        functionality_category = Room.set_self_privilege_functionality_tree.get(room_classification, {}).get(privilege_action, {})

        functionality = functionality_category.get(permission_involved, None)

        if functionality is None:
            raise InsufficientPermissions("You do not have permissions to do that.")

        if client.allowed(functionality):
            self._client_change_privilege(client, client, requested_privilege)
        else:
            raise InsufficientPermissions(functionality.denied_message)

    def _set_others_privilege(self, client, target, requested_privilege):
        raise GenericError("Setting other player privileges isn't currently implemented.")

    def _client_try_set_privilege(self, client, target, requested_privilege):
        if client is target:
            return self._set_self_privilege(client, requested_privilege)
        else:
            return self._set_others_privilege(client, target, requested_privilege)

    def _update_current_masters(self):
        self._broadcaster.current_masters(self.mastermode, self.clients)

    def _finalize_demo_recording(self):
        self.demo_recorder.write("/tmp/abaracada.dmo")

    def _initialize_demo_recording(self):
        self.demo_recorder.initialize_demo_recording()
