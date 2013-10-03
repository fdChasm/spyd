import os.path
import re

import simplejson


class ConfigurationError(Exception): pass

def load_json_to_dictionary(json_filename):
    with open(json_filename, 'rb') as f:
        try:
            return simplejson.load(f)
        except ValueError as e:
            message = "{}: {}".format(json_filename, e.message)
            raise ConfigurationError(message)

json_file_uri_pattern = re.compile('^file:\/\/(.*\.json)$')

def resolve_referenced_configs(config_dictionary):
    for k, v in config_dictionary.items():
        if isinstance(v, dict):
            resolve_referenced_configs(v)
        else:
            try:
                match = json_file_uri_pattern.match(v)
                if match:
                    config_filename = os.path.abspath(match.group(1))
                    config_dictionary[k] = load_json_to_dictionary(config_filename)
                    resolve_referenced_configs(config_dictionary[k])
            except TypeError:
                pass

def config_loader(config_filename):
    raw_config = load_json_to_dictionary(config_filename)
    resolve_referenced_configs(raw_config)
    return raw_config
