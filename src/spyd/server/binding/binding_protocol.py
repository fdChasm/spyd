from twisted.internet import protocol, defer

import cPickle as pickle
import struct

header_packer = struct.Struct('Q')
MSGLEN_SIZE = header_packer.size

'''
For info about what you can do with binding_protocol.transport
see: http://twistedmatrix.com/documents/13.0.0/core/howto/process.html
'''

class BindingProtocol(protocol.ProcessProtocol):
    def __init__(self, write_rate_aggregator, read_rate_aggregator):
        self.receive_buffer = bytearray()
        self.next_request_id = 0
        self.pending_requests = {}

        self.write_rate_aggregator = write_rate_aggregator
        self.read_rate_aggregator = read_rate_aggregator

    def send(self, message):
        request, d = self._create_request(message)

        write_buffer = bytearray(MSGLEN_SIZE)

        data = pickle.dumps(request, protocol=pickle.HIGHEST_PROTOCOL)
        msglen = len(data)
        header_packer.pack_into(write_buffer, 0, msglen)

        write_buffer.extend(data)

        data_to_write = str(write_buffer)
        self.transport.write(data_to_write)

        self.write_rate_aggregator.tick(len(data_to_write))

        return d

    def outReceived(self, data):
        self.read_rate_aggregator.tick(len(data))
        self.receive_buffer.extend(data)
        messages = self._pop_messages()
        for message in messages:
            message_type = message.get('type', None)
            if message_type == 'response':
                self._handle_response(message)
            else:
                self.factory.message_received(self, message)

    def connectionMade(self): pass
    def errReceived(self, data): print data
    def inConnectionLost(self): pass
    def outConnectionLost(self): pass
    def errConnectionLost(self): pass

    def processExited(self, reason):
        print "binding process exited. Status: {reason.value.exitCode}".format(reason=reason)

    def processEnded(self, reason):
        print "binding process ended. Status: {reason.value.exitCode}".format(reason=reason)

    def _pop_messages(self):
        messages = []
        while True:
            message = self._pop_message()
            if message is None: break
            messages.append(message)
        return messages

    def _pop_message(self):
        message = None
        buflen = len(self.receive_buffer)
        if buflen >= MSGLEN_SIZE:
            msglen = header_packer.unpack_from(buffer(self.receive_buffer))[0]
            if buflen >= MSGLEN_SIZE + msglen:
                data = str(self.receive_buffer[MSGLEN_SIZE:MSGLEN_SIZE + msglen])
                message = pickle.loads(data)
                del self.receive_buffer[:MSGLEN_SIZE + msglen]
        return message

    def _get_request_id(self):
        rid = self.next_request_id
        self.next_request_id += 1
        return rid

    def _create_request(self, message):
        rid = self._get_request_id()
        request = {'rid': rid}
        request.update(message)
        d = defer.Deferred()
        self.pending_requests[rid] = d
        return request, d

    def _handle_response(self, message):
        rid = message['rid']
        result = message['result']
        d = self.pending_requests.pop(rid)
        d.callback(result)
