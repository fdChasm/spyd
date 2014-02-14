import glob
import json
import os.path
import sys

from cube2map.read_map_meta_data import read_map_data


unbuffered = os.fdopen(sys.stdout.fileno(), 'w', 0)

def to_netstring(message):
    return "{}:{},".format(len(message), message)

def map_filename_to_map_name(map_filename):
    return os.path.splitext(os.path.basename(map_filename))[0]

def handle_message(message):
    method = message['method']

    if method == u'read_map_data':
        map_path = message['args'][0]

        if os.path.exists(map_path):
            result = read_map_data(map_path)
        else:
            result = None

    elif method == u'read_map_names':
        map_glob_expression = message['args'][0]
        map_filenames = glob.glob(map_glob_expression)
        result = map(map_filename_to_map_name, map_filenames)

    else:
        return unbuffered.write(to_netstring(json.dumps({'error': 'Unknown method.', 'reqid': message[u'reqid']})))

    unbuffered.write(to_netstring(json.dumps({'result': result, 'reqid': message[u'reqid']})))

lenbuffer = bytearray()
while True:
    c = sys.stdin.read(1)
    if c in "0123456789":
        lenbuffer.extend(c)
    elif c == ':':
        data = sys.stdin.read(int(lenbuffer) + 1)
        lenbuffer = bytearray()
        assert(data[-1] == ',')
        message = json.loads(data[:-1])
        handle_message(message)
    else:
        raise Exception("Unexpected character while reading length.")
