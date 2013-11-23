import gzip
import struct

from cube2stress.protocol.message_processor import MessageProcessor


def get_demo_data(demo_filename):
    "Returns a list of ClientSession objects."

    mp = MessageProcessor()

    with gzip.open(demo_filename) as f:
        DEMO_MAGIC, demo_version, protocol_version = struct.unpack("16sii", f.read(24))
        print DEMO_MAGIC, demo_version, protocol_version

        while True:
            d = f.read(12)
            if len(d) < 12:
                # print "breaking on read packet header '{}'".format(d)
                break

            millis, channel, length = struct.unpack("iii", d)

            d = f.read(length)
            if len(d) < length:
                # print "breaking on read packet '{}'".format(d)
                break

            messages = mp.process(channel, d)

            for message in messages:
                print millis, message
