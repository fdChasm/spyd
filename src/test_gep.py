import itertools
import json
import time

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver

import cube2crypto


private_key = "81a838d411f32284ce4d9bfee2af62d62db0308fa73a6b2f"

request_id = itertools.count()

class GEPProtocol(NetstringReceiver):

    def __init__(self):
        self._callbacks = {}

    def stringReceived(self, data):
        message = json.loads(data)
        self._message_received(message)

    def _message_received(self, message):
        respid = message.pop('respid', None)
        callback = self._callbacks.pop(respid, self._default_callback)
        callback(message)

    def connectionMade(self):
        Protocol.connectionMade(self)
        self.request({"msgtype": "gep.connect", "username": "bob", "domain": "example.com"}, self._on_connect_response)

    def connectionLost(self, reason):
        print "connection lost"
        if reactor.running:
            reactor.stop()

    def request(self, message, callback):
        reqid = request_id.next()
        message['reqid'] = reqid
        self._callbacks[reqid] = callback
        self.send(message)

    def send(self, message):
        self.sendString(json.dumps(message))

    def _default_callback(self, message):
        print "message:", json.dumps(message)

    def _on_connect_response(self, message):
        challenge = str(message['challenge'])
        answer = str(cube2crypto.answer_challenge(private_key, challenge))
        self.request({'msgtype': 'gep.answer', 'answer': answer}, self._on_answer_response)

    def _on_answer_response(self, message):
        if message.get('status', None) == u'success':
            self.request({'msgtype': 'gep.subscribe', 'event_stream': 'spyd.game.player.chat'}, self._on_subscribe_response)
            self.request({'msgtype': 'gep.subscribe', 'event_stream': 'spyd.game.player.connect'}, self._on_subscribe_response)
            self.request({'msgtype': 'gep.ping', 'time': time.time()}, self._on_ping_response)
        else:
            self.transport.loseConnection()

    def _on_subscribe_response(self, message):
        print "subscribe request:", message

    def _on_ping_response(self, message):
        start_time = message['client_time']
        echo_time = message['server_time']
        now_time = time.time()

        cts = (echo_time - start_time) * 1000
        stc = (now_time - echo_time) * 1000
        rnd = (now_time - start_time) * 1000

        print "ping response: cts: {:.4f} ms, stc: {:.4f} ms, rnd: {:.4f} ms".format(cts, stc, rnd)



class GEPClientFactory(ClientFactory):

    protocol = GEPProtocol


def poetry_main():
    host, port = "127.0.0.1", 28788

    factory = GEPClientFactory()
    reactor.connectTCP(host, port, factory)

    reactor.run()

if __name__ == '__main__':
    poetry_main()
