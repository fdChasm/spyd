from mock import MagicMock
import re
import unittest

from cube2common.constants import message_types
from spyd.game.client.client import Client
from spyd.game.client.client_message_handling_base import ClientMessageHandlingBase
from spyd.game.room.room import Room
from spyd.protocol.server_read_stream_protocol import sauerbraten_stream_spec
from spyd.utils.ping_buffer import PingBuffer


message_handler_method_pattern = re.compile("^N_")

class TestClientMessageHandlers(unittest.TestCase):
    def setUp(self):
        self.client_message_handling_base = ClientMessageHandlingBase()
        self.handled_message_types = self.client_message_handling_base._message_handlers.keys()

    def test_all_message_types_handled(self):

        for message_type in sauerbraten_stream_spec.message_types.iterkeys():
            message_type_name = message_types.by_value(message_type)
            self.assertIn(message_type_name, self.handled_message_types, "No handler for message type {}".format(message_type_name))
            
    def test_all_message_handlers_call_valid_room_handlers(self):
        client = MagicMock(spec=Client)
        
        room = MagicMock(name="Room", spec=Room)
        
        client.room = room
        client.ping_buffer = MagicMock(spec=PingBuffer)

        for handled_message_type in self.handled_message_types:
            message = MagicMock(spec_set=dict)
            
            self.client_message_handling_base._message_received(handled_message_type, message)
