import json

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver

import cube2crypto
import itertools


private_key = "81a838d411f32284ce4d9bfee2af62d62db0308fa73a6b2f"

request_id = itertools.count()

class GEPProtocol(NetstringReceiver):
    
    def __init__(self):
        self._callbacks = {}

    def stringReceived(self, data):
        message = json.loads(data)
        self._message_received(message)
    
    def _message_received(self, message):
        reqid = message.pop('reqid', None)
        callback = self._callbacks.pop(reqid, self._default_callback)
        callback(message)
        
    def connectionMade(self):
        Protocol.connectionMade(self)
        self.request({"msgtype": "connect", "username": "bob", "domain": "example.com"}, self._on_connect_response)

    def connectionLost(self, reason):
        print "connection lost"
        
    def request(self, message, callback):
        reqid = request_id.next()
        message['reqid'] = request_id.next()
        self._callbacks[reqid] = callback
        self.send(message)
        
    def send(self, message):
        self.sendString(json.dumps(message))

    def _default_callback(self, message):
        print "message:", message
        
    def _on_connect_response(self, message):
        challenge = str(message['challenge'])
        answer = str(cube2crypto.answer_challenge(private_key, challenge))
        self.request({'msgtype': 'answer', 'answer': answer}, self._on_answer_response)
    
    def _on_answer_response(self, message):
        if message.get('status', None) == u'success':
            self.request({'msgtype': 'subscribe', 'event_stream': 'spyd.game.player.chat'}, self._on_subscribe_response)
        else:
            self.transport.loseConnection()
        
    def _on_subscribe_response(self, message):
        print "subscribe request:", message
        


class GEPClientFactory(ClientFactory):

    protocol = GEPProtocol


def poetry_main():

    from twisted.internet import reactor

    host, port = "127.0.0.1", 28788
    
    factory = GEPClientFactory()
    reactor.connectTCP(host, port, factory)

    reactor.run()

if __name__ == '__main__':
    poetry_main()
