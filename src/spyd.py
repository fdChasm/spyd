# You can run this .tac file directly with:
#    twistd -ny service.tac
#from twisted.python import log
import logging

#observer = log.PythonLoggingObserver()
#observer.start()
logging.basicConfig(level=logging.DEBUG)

from twisted.application import service
from twisted.internet import reactor, defer
from twisted.application.internet import TCPClient  # @UnresolvedImport

from cube2common.constants import disconnect_types
from sauerpyd.client.client_factory import ClientFactory
from sauerpyd.client.client_number_provider import get_client_number_provider
from sauerpyd.master_client.master_client_bindings import MasterClientBindings
from sauerpyd.master_client.master_client_factory import MasterClientFactory
from sauerpyd.protocol.message_processor import MessageProcessor
from sauerpyd.punitive_effects.punitive_model import PunitiveModel
from sauerpyd.room.room_bindings import RoomBindings
from sauerpyd.room.room_factory import RoomFactory
from sauerpyd.room.room_manager import RoomManager
from sauerpyd.server_message_formatter import notice
from server.binding.binding_factory import BindingFactory
from server.binding.binding_service import BindingService
from server.client_manager import ClientManager
from server.lan_info.lan_info_service import LanInfoService


config = {
    'lan_findable': True,
    'room_bindings': {
        'lobby': {
                      'type': 'public',
                      'interface': '127.0.0.1',
                      'port': 28785,
                      'masterserver': ('localhost', 28787, True),
                      'maxclients': 512,
                      'maxplayers': 16,
                      'maxdown': 0,
                      'maxup': 0,
                  },
        'bored': {
                      'type': 'public',
                      'interface': '127.0.0.1',
                      'port': 10000,
                      'masterserver': ('localhost', 28787, False),
                      'maxclients': 512,
                      'maxplayers': 16,
                      'maxdown': 0,
                      'maxup': 0,
                      'public': True,
                  }
    }
}

root_service = service.MultiService()

room_factory = RoomFactory(config)
room_manager = RoomManager()
room_bindings = RoomBindings()

punitive_model = PunitiveModel()

master_client_bindings = MasterClientBindings()

message_processor = MessageProcessor()

client_number_provider = get_client_number_provider(config)
client_factory = ClientFactory(client_number_provider, room_bindings, master_client_bindings)
client_manager = ClientManager(client_factory, message_processor)

binding_factory = BindingFactory(client_manager)
binding_service = BindingService(binding_factory)
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
    room_type = room_config.get('type', 'public')
    default_room = room_config.get('default', True)
    
    room = room_factory.build_room(room_name, room_type)
    
    binding_service.add_binding(interface, port, maxclients, maxdown, maxup)
    room_manager.add_room(room)
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
    #reactor.callLater(1, printer, "2...")
    #reactor.callLater(2, printer, "1...")
    #reactor.callLater(3, printer, "0...")
    d = defer.Deferred()
    reactor.callLater(1, d.callback, 1)
    return d

reactor.addSystemEventTrigger("before", "shutdown", shutdown)

application = service.Application("Spyd Sauerbraten Server")
root_service.setServiceParent(application)