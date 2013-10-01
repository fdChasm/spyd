import cPickle
import glob
import os
import sys

from cube2map.read_map_meta_data import read_map_data


if len(sys.argv) < 3:
    print "Usage: {} \"path/to/maps/*.ogz\" path/to/store/meta_data.pkl".format(sys.argv[0])
    sys.exit(1)

map_glob_expression = sys.argv[1]
#map_glob_expression = "{}/Desktop/sauerbraten/packages/base/*.ogz".format(os.environ['HOME'])

target_pickle_file = sys.argv[2]

map_filenames = glob.glob(map_glob_expression)

map_meta_data = {}
failed_maps = []

for map_filename in map_filenames:
    map_name, _ = os.path.splitext(os.path.basename(map_filename))
    try:
        map_meta_data[map_name] = read_map_data(map_filename)
    except:
        failed_maps.append(map_filename)

with open(target_pickle_file, 'wb') as f:
    cPickle.dump(map_meta_data, f)

print "The following maps failed to load; {}".format(failed_maps)
print "Saved meta data for {} maps.".format(len(map_meta_data))
