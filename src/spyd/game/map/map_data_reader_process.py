import glob
import json
import os.path
import sys

from cube2map.read_map_meta_data import read_map_data


def map_filename_to_map_name(map_filename):
    return os.path.splitext(os.path.basename(map_filename))[0]

if len(sys.argv) < 3 or sys.argv[1] not in ('-l', '-d'):
    sys.exit(1)

if sys.argv[1] == '-d':
    map_path = sys.argv[2]
    if os.path.exists(map_path):
        result = read_map_data(map_path)
        sys.stdout.write(json.dumps(result))

elif sys.argv[1] == '-l':
    map_glob_expression = sys.argv[2]
    map_filenames = glob.glob(map_glob_expression)
    result = map(map_filename_to_map_name, map_filenames)
    sys.stdout.write(json.dumps(result))
