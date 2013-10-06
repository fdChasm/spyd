import logging
import os.path

from twisted.application import service
from twisted.application.internet import TCPClient
from twisted.internet import reactor, defer

from cube2common.constants import disconnect_types
from server.binding.binding_factory import BindingFactory
from server.binding.binding_service import BindingService
from server.client_manager import ClientManager
from server.lan_info.lan_info_service import LanInfoService
from spyd.config_loader import config_loader
from spyd.game.client.client_factory import ClientFactory
from spyd.game.client.client_number_provider import get_client_number_provider
from spyd.game.command.command_executer import CommandExecuter
from spyd.game.map.map_meta_data_accessor import MapMetaDataAccessor
from spyd.game.room.room_bindings import RoomBindings
from spyd.game.room.room_factory import RoomFactory
from spyd.game.room.room_manager import RoomManager
from spyd.game.server_message_formatter import notice
from spyd.master_client.master_client_bindings import MasterClientBindings
from spyd.master_client.master_client_factory import MasterClientFactory
from spyd.permissions.permission_resolver import PermissionResolver
from spyd.protocol.message_processor import MessageProcessor
from spyd.punitive_effects.punitive_model import PunitiveModel
from spyd.utils.value_model import ValueModel


def make_service(options):
    binding_path = os.path.abspath(options.get('bindingpath'))
    
    home_directory = os.path.abspath(options.get('homedir'))
    os.chdir(home_directory)
    
    config_filename = os.path.abspath(options.get('config'))
    config = config_loader(config_filename)
    
    logging.basicConfig(level=logging.DEBUG)

    root_service = service.MultiService()
    
    server_name_model = ValueModel(config.get('server_name', '123456789ABCD'))
    
    packages_directory = config.get('packages_directory', "{}/git/spyd/packages".format(os.environ['HOME']))
    map_meta_data_accessor = MapMetaDataAccessor(packages_directory)
    
    command_executer = CommandExecuter()

    room_manager = RoomManager()
    room_factory = RoomFactory(config, room_manager, server_name_model, map_meta_data_accessor, command_executer)
    room_bindings = RoomBindings()

    punitive_model = PunitiveModel()
    
    permission_resolver = PermissionResolver.from_dictionary(config.get('permissions'))

    master_client_bindings = MasterClientBindings()

    message_processor = MessageProcessor()

    client_number_provider = get_client_number_provider(config)
    client_factory = ClientFactory(client_number_provider, room_bindings, master_client_bindings, permission_resolver)
    client_manager = ClientManager(client_factory, message_processor)

    binding_factory = BindingFactory(client_manager)
    binding_service = BindingService(binding_factory, binding_path)
    binding_service.setServiceParent(root_service)

    lan_info_service = LanInfoService(config['lan_findable'])
    lan_info_service.setServiceParent(root_service)

    for room_name, room_config in config['room_bindings'].iteritems():
        interface = room_config['interface']
        port = room_config['port']
        masterserver = room_config.get('masterserver', None)
        maxclients = room_config['maxclients']
        maxdown = room_config.get('maxdown', 0)
        maxup = room_config.get('maxup', 0)
        room_type = room_config.get('type', 'permanent')
        default_room = room_config.get('default', True)

        room = room_factory.build_room(room_name, room_type)

        binding_service.add_binding(interface, port, maxclients, maxdown, maxup)
        room_bindings.add_room(port, room, default_room)
        lan_info_service.add_lan_info_for_room(room, interface, port)

        if masterserver is not None:
            master_host, master_port, default_master = masterserver

            master_client = MasterClientFactory(punitive_model, master_host, port)
            master_client_service = TCPClient(master_host, master_port, master_client)
            master_client_service.setServiceParent(root_service)
            master_client_bindings.add_master_client(port, master_client, default_master)

    def printer(s):
        print s

    def shutdown():
        print "Shutting down in 3 seconds to allow clients to disconnect."
        client_manager.disconnect_all(disconnect_type=disconnect_types.DISC_NONE, message=notice("Server going down. Please come back when it is back up."))
        # reactor.callLater(1, printer, "2...")
        # reactor.callLater(2, printer, "1...")
        # reactor.callLater(3, printer, "0...")
        d = defer.Deferred()
        reactor.callLater(1, d.callback, 1)
        return d

    reactor.addSystemEventTrigger("before", "shutdown", shutdown)

    return root_service
