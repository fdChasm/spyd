import logging
import os

from twisted.application import service
from twisted.internet import reactor, defer
import txCascil
from txCascil.events import EventSubscriptionFulfiller

from cube2common.constants import disconnect_types
from cube2protocol.sauerbraten.collect.server_read_message_processor import ServerReadMessageProcessor
from server.lan_info.lan_info_service import LanInfoService
from spyd.authentication.auth_world_view_factory import AuthWorldViewFactory, ANY
from spyd.authentication.master_client_service_factory import MasterClientServiceFactory
from spyd.game.client.client_factory import ClientFactory
from spyd.game.client.client_number_provider import get_client_number_handle_provider
from spyd.game.command.command_executer import CommandExecuter
from spyd.game.map.async_map_meta_data_accessor import AsyncMapMetaDataAccessor
from spyd.game.room.room_bindings import RoomBindings
from spyd.game.room.room_factory import RoomFactory
from spyd.game.room.room_manager import RoomManager
from spyd.game.server_message_formatter import notice
from spyd.permissions.permission_resolver import PermissionResolver
from spyd.punitive_effects.punitive_model import PunitiveModel
from spyd.registry_manager import RegistryManager
from spyd.server.binding.binding_service import BindingService
from spyd.server.binding.client_protocol_factory import ClientProtocolFactory
import spyd.server.gep_message_handlers  # @UnusedImport
from spyd.server.metrics import get_metrics_service
from spyd.server.metrics.execution_timer import ExecutionTimer
from spyd.utils.value_model import ValueModel


logger = logging.getLogger(__name__)

def get_package_dir(config):
    return config.get('packages_directory', "{}/git/spyd/packages".format(os.environ['HOME']))

class SpydServer(object):
    def __init__(self, config):
        self.root_service = service.MultiService()

        self.metrics_service = get_metrics_service(config)
        self.metrics_service.setServiceParent(self.root_service)

        self.server_name_model = ValueModel(config.get('server_name', '123456789ABCD'))
        self.server_info_model = ValueModel(config.get('server_info', "An Spyd Server!"))

        sauerbraten_package_dir = get_package_dir(config)
        map_meta_data_accessor = AsyncMapMetaDataAccessor(sauerbraten_package_dir)
        print "Using package directory; {!r}".format(sauerbraten_package_dir)

        self.event_subscription_fulfiller = EventSubscriptionFulfiller()

        command_executer = CommandExecuter(self)

        self.room_manager = RoomManager()
        self.room_factory = RoomFactory(config, self.room_manager, self.server_name_model, map_meta_data_accessor, command_executer, self.event_subscription_fulfiller, self.metrics_service)
        self.room_bindings = RoomBindings()

        self.permission_resolver = PermissionResolver.from_dictionary(config.get('permissions'))

        self.punitive_model = PunitiveModel()
        self.master_client_service_factory = MasterClientServiceFactory(self.punitive_model)
        self.auth_world_view_factory = AuthWorldViewFactory()

        self.message_processor = ServerReadMessageProcessor()
        message_processing_execution_timer = ExecutionTimer(self.metrics_service, 'process_message', 1.0)

        self.connect_auth_domain = config.get('connect_auth_domain', '')

        client_number_handle_provider = get_client_number_handle_provider(config)
        self.client_factory = ClientFactory(client_number_handle_provider, self.room_bindings, self.auth_world_view_factory, self.permission_resolver, self.event_subscription_fulfiller, self.connect_auth_domain, self.punitive_model)

        self.client_protocol_factory = ClientProtocolFactory(self.client_factory, self.message_processor, config.get('client_message_rate_limit', 200), message_processing_execution_timer)

        self.binding_service = BindingService(self.client_protocol_factory, self.metrics_service)
        self.binding_service.setServiceParent(self.root_service)

        self.lan_info_service = LanInfoService(self.room_manager, config['lan_findable'], config['ext_info'])
        self.lan_info_service.setServiceParent(self.root_service)

        self._initialize_master_clients(config)
        self._initialize_rooms(config)
        self._initialize_gep_endpoints(config)

        reactor.addSystemEventTrigger("before", "shutdown", self._before_shutdown, config)

    def _initialize_rooms(self, config):
        default_room_name = config.get('default_room')

        max_duplicate_peers = config.get('max_duplicate_peers', 10)

        for room_name, room_config in config['room_bindings'].iteritems():
            interface = room_config['interface']
            port = room_config['port']
            maxclients = room_config['maxclients']
            maxdown = room_config.get('maxdown', 0)
            maxup = room_config.get('maxup', 0)
            room_type = room_config.get('type', 'permanent')
            default_room = room_name == default_room_name

            room = self.room_factory.build_room(room_name, room_type)

            self.binding_service.add_binding(interface, port, maxclients, maxdown, maxup, max_duplicate_peers)
            self.room_bindings.add_room(port, room, default_room)
            self.lan_info_service.add_lan_info_for_room(room, interface, port)

    def _initialize_master_clients(self, config):
        for master_server_config in config['master_servers']:
            register_port = master_server_config.get('register_port', ANY)
            master_client_service = self.master_client_service_factory.build_master_client_service(master_server_config)
            self.auth_world_view_factory.register_auth_service(master_client_service, register_port)
            master_client_service.setServiceParent(self.root_service)
            
    def _initialize_gep_endpoints(self, config):
        message_handlers = {}
        for message_handler_registration in RegistryManager.get_registrations('gep_message_handler'):
            message_handler = message_handler_registration.registered_object
            if message_handler.msgtype in message_handlers:
                raise Exception("Duplicate message handler registered.")
            message_handlers[message_handler.msgtype] = message_handler

        gep_service_factory = txCascil.ServerServiceFactory()
        for gep_config in config['gep_endpoints'].itervalues():
            gep_service = gep_service_factory.build_service(self, gep_config, message_handlers, self.permission_resolver, self.event_subscription_fulfiller)
            gep_service.setServiceParent(self.root_service)

    def _before_shutdown(self, config):
        shutdown_countdown = config.get('shutdown_countdown', 3)

        reactor.callLater(0.1, logger.spyd_event, "Shutting down in {} seconds to allow clients to disconnect.".format(shutdown_countdown))
        self.client_protocol_factory.disconnect_all(disconnect_type=disconnect_types.DISC_NONE, message=notice("Server going down. Please come back when it is back up."))

        for i in xrange(shutdown_countdown):
            reactor.callLater(shutdown_countdown - i, logger.spyd_event, "{}...".format(i))
        d = defer.Deferred()
        reactor.callLater(shutdown_countdown + 0.1, d.callback, 1)
        return d
