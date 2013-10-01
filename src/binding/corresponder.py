"""
[int64 message_size][pickled_data]
"""
import os
import cPickle as pickle
import struct
import select

header_packer = struct.Struct('Q')
MSGLEN_SIZE = header_packer.size

class CorrespondenceEnded(Exception): pass

class Corresponder(object):
    def __init__(self, incoming_fd, outgoing_fd):
        self.incoming_fd = incoming_fd
        self.outgoing_fd = outgoing_fd
        
        self.read_buffer = bytearray()
        self.write_buffer = bytearray()
    
    def send(self, message):
        write_buffer = bytearray(MSGLEN_SIZE)
        data = pickle.dumps(message, protocol=pickle.HIGHEST_PROTOCOL)
        msglen = len(data)
        header_packer.pack_into(write_buffer, 0, msglen)
        write_buffer.extend(data)
        self._write_message(write_buffer)
        self.flush()
    
    def receive(self, timeout):
        self._read(timeout)
        messages = self._pop_messages()
        return messages
    
    def flush(self):
        "Writes data to the output stream. If in blocking_write mode then this will block until the write_buffer is empty."
        while len(self.write_buffer) > 0:
            _, _, _ = select.select((), (self.outgoing_fd,), (), 0)
            written = os.write(self.outgoing_fd, self.write_buffer)
            self.write_buffer = self.write_buffer[written:]
    
    def _read(self, timeout):
        #sys.stderr.write("_read before select\n")
        rl, _, _ = select.select((self.incoming_fd,), (), (), timeout)
        #sys.stderr.write("_read after select\n")
        if len(rl):
            data = os.read(rl[0], 4096)
            if len(data) == 0:
                raise CorrespondenceEnded()
            self.read_buffer.extend(data)
        
    def _pop_messages(self):
        messages = []
        while True:
            message = self._pop_message()
            if message is None: break
            messages.append(message)
        return messages
    
    def _pop_message(self):
        message = None
        buflen = len(self.read_buffer)
        if buflen >= MSGLEN_SIZE:
            msglen = header_packer.unpack_from(buffer(self.read_buffer))[0]
            if buflen >= MSGLEN_SIZE+msglen:
                data = str(self.read_buffer[MSGLEN_SIZE:MSGLEN_SIZE+msglen])
                message = pickle.loads(data)
                del self.read_buffer[:MSGLEN_SIZE+msglen]
        return message
    
    def _write_message(self, raw_message):
        self.write_buffer.extend(raw_message)
