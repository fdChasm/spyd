import contextlib
from contextlib import contextmanager
from mock import patch, MagicMock
from spyd.game.player.player_state import PlayerState
from spyd.game.client.client import Client

class PlayerTestContext(object):
    def __init__(self, test_case, player):
        self.test_case = test_case
        self.player = player
        self.sendbuffers = []
        
    def enter_room(self, room):
        entry_context = room.get_entry_context(self.player.client, self.player)
        room.client_enter(entry_context)
        
    def leave_room(self, room):
        room.client_leave(self.player.client)
        
    def clear_received_messages(self):
        del self.sendbuffers[:]
        
    def get_received_messages_of_type(self, message_type):
        messages_of_type = []
        for sendbuffer in self.sendbuffers:
            for received_message_type, received_message_data in sendbuffer:
                if received_message_type == message_type:
                    messages_of_type.append(received_message_data)
        return messages_of_type
    
    def get_all_received_messages(self):
        messages = []
        for sendbuffer in self.sendbuffers:
            messages.extend(sendbuffer)
        return messages
    
    def has_received_message_of_type(self, message_type):
        has_received_message = False
        for sendbuffer in self.sendbuffers:
            for received_message_type, _ in sendbuffer:
                if received_message_type == message_type:
                    has_received_message = True
                    break
            if has_received_message: break
        return has_received_message
    
    def assertHasReceivedMessageOfType(self, message_type):
        has_received_message = self.has_received_message_of_type(message_type)
        self.test_case.assertTrue(has_received_message, 'Message of type {} not received.'.format(message_type))
        
    def assertHasNotReceivedMessageOfType(self, message_type):
        has_received_message = self.has_received_message_of_type(message_type)
        self.test_case.assertFalse(has_received_message, 'Message of type {} was received.'.format(message_type))

@contextmanager
def create_mock_player(test_case, cn):
    with patch('spyd.game.player.player.Player', spec=True) as player:
        player.client = MagicMock(spec=Client)
        player.client.cn = cn
        player.client.get_player = lambda: player
        player.client.players = {cn: player}
        player.isai = False
        player.cn = cn
        player.state = PlayerState()
        
        player_test_context = PlayerTestContext(test_case, player)
        
        player_test_context.sendbuffers = []
        player.state.messages = []
        
        def sendbuffer(channel, reliable):
            sendbuffer = []
            yield sendbuffer
            player.send(channel, sendbuffer, reliable)
        player.sendbuffer = contextlib.contextmanager(sendbuffer)
        player.client.sendbuffer = player.sendbuffer
        
        def send(channel, data, reliable):
            player_test_context.sendbuffers.append(data)
        player.send = send
        player.client.send = send
        
        yield player_test_context
    