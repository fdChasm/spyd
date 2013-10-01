import os
import simplejson

class ConfigurationError(Exception): pass

def json_to_dict(filename):
    with open(os.path.abspath(filename), 'rb') as f:
        try:
            return simplejson.load(f)
        except ValueError as e:
            message = "{}: {}".format(filename, e.message)
            raise ConfigurationError(message)

config = {
    'lan_findable': True,
    'packages_directory': '/opt/sauerbraten/packages',
    'room_bindings': {
        'lobby': {
                      'type': 'public',
                      'interface': '127.0.0.1',
                      'port': 28785,
                      'masterserver': ('localhost', 28787, True),
                      'maxclients': 512,
                      'maxplayers': 16,
                      'maxdown': 0,
                      'maxup': 0,
                  },
        'bored': {
                      'type': 'public',
                      'interface': '127.0.0.1',
                      'port': 10000,
                      'masterserver': ('localhost', 28787, False),
                      'maxclients': 512,
                      'maxplayers': 16,
                      'maxdown': 0,
                      'maxup': 0,
                      'public': True,
                  }
    },
    'room_types': {
       'default': {
           'map_rotation': json_to_dict('map_rotation.json'),
       },
       'public': {
           'map_rotation': json_to_dict('map_rotation.json'),
       }
   }
}
