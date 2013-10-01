import unittest
from sauerpyd.protocol.server_read_stream_protocol import sauerbraten_stream_spec
from cube2common.constants import message_types

from sauerpyd.client.client_message_handling_base import ClientMessageHandlingBase
from mock import MagicMock
import re
from sauerpyd.room.room import Room
from sauerpyd.client.client import Client
from utils.ping_buffer import PingBuffer

message_handler_method_pattern = re.compile("^N_")

class TestClientMessageHandlers(unittest.TestCase):
    def setUp(self):
        pass

    def test_all_message_types_handled(self):
        handled_message_types = filter(message_handler_method_pattern.match, dir(ClientMessageHandlingBase))
        for message_type in sauerbraten_stream_spec.message_types.iterkeys():
            message_type_name = message_types.by_value(message_type)
            self.assertIn(message_type_name, handled_message_types, "No handler for message type {}".format(message_type_name))
            
    def test_all_message_handlers_call_valid_room_handlers(self):
        handled_message_types = filter(message_handler_method_pattern.match, dir(ClientMessageHandlingBase))

        client = MagicMock(spec=Client)
        
        room = MagicMock(name="Room", spec=Room)
        
        client.room = room
        client.ping_buffer = MagicMock(spec=PingBuffer)

        for handled_message_type in handled_message_types:
            message = MagicMock(spec_set=dict)
            
            handler = getattr(ClientMessageHandlingBase, handled_message_type)
            handler(client, message)