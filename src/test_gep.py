import itertools
import json
import time

import clj
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver

import cube2crypto


PACKER = json

private_key = "81a838d411f32284ce4d9bfee2af62d62db0308fa73a6b2f"

request_id = itertools.count()

class GEPProtocol(NetstringReceiver):

    def __init__(self):
        self._callbacks = {}

    def stringReceived(self, data):
        message = PACKER.loads(data)
        self._message_received(message)

    def _message_received(self, message):
        print json.dumps(message)
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
        print json.dumps(message)
        self.send(message)

    def send(self, message):
        self.sendString(PACKER.dumps(message))

    def _default_callback(self, message):
        if message['msgtype'] == u'gep.event':
            event_data = message['event_data']
            event_stream = message['event_stream']

            event_stream_handler_name = "_on_event_{}".format(event_stream.replace('.', '_'))
            handler = getattr(self, event_stream_handler_name, self._default_event_handler)
            handler(message, event_data)
        else:
            print "message:", message

    def _default_event_handler(self, message, event_data):
        print "event", message

    def _on_connect_response(self, message):
        challenge = str(message['challenge'])
        answer = str(cube2crypto.answer_challenge(private_key, challenge))
        self.request({'msgtype': 'gep.answer', 'answer': answer}, self._on_answer_response)

    def _on_answer_response(self, message):
        if message.get('status', None) == u'success':
            self.request({'msgtype': 'gep.subscribe', 'event_stream': 'spyd.game.player.chat'}, self._on_subscribe_response)
            self.request({'msgtype': 'gep.subscribe', 'event_stream': 'spyd.game.player.connect'}, self._on_subscribe_response)
            self.request({'msgtype': 'gep.ping', 'time': int(time.time() * 1000000)}, self._on_ping_response)
        else:
            self.transport.loseConnection()

    def _on_subscribe_response(self, message):
        print "subscribe request:", message

    def _on_ping_response(self, message):
        start_time = message['client_time']
        echo_time = message['server_time']
        now_time = int(time.time() * 1000000)

        cts = (echo_time - start_time) / 1000.0
        stc = (now_time - echo_time) / 1000.0
        rnd = (now_time - start_time) / 1000.0

        print "ping response: cts: {:.4f} ms, stc: {:.4f} ms, rnd: {:.4f} ms".format(cts, stc, rnd)

    def _on_player_info_response(self, message):
        pass

    def _on_room_info_response(self, message):
        pass

    def _on_event_spyd_game_player_connect(self, message, event_data):
        player_uuid = event_data['player']
        reactor.callLater(1, self.request, {'msgtype': 'gep.get_player_info', 'player': player_uuid}, self._on_player_info_response)

        room_name = event_data['room']
        reactor.callLater(1, self.request, {'msgtype': 'gep.get_room_info', 'room': room_name}, self._on_room_info_response)

        reactor.callLater(2, self.request, {'msgtype': 'gep.set_player_room', 'room': 'xyz', 'player': player_uuid, 'message': 'get used to it.'}, self._on_room_info_response)

        reactor.callLater(5, self.request, {'msgtype': 'gep.set_room_paused', 'room': 'xyz', 'pause': 1, 'message': 'Told you guys to get used to it.'}, self._on_room_info_response)

        reactor.callLater(10, self.request, {'msgtype': 'gep.set_room_paused', 'room': 'xyz', 'pause': 0, 'message': 'Told you guys to get used to it.'}, self._on_room_info_response)


class GEPClientFactory(ClientFactory):

    protocol = GEPProtocol


def poetry_main():
    host, port = "127.0.0.1", 28788

    factory = GEPClientFactory()
    reactor.connectTCP(host, port, factory)

    reactor.run()

if __name__ == '__main__':
    poetry_main()
