import simplejson


class ConfigurationError(Exception): pass

def load_json_to_dictionary(json_filename):
    with open(json_filename, 'rb') as f:
        try:
            return simplejson.load(f)
        except ValueError as e:
            message = "{}: {}".format(json_filename, e.message)
            raise ConfigurationError(message)

def config_loader(config_filename):
    raw_config = load_json_to_dictionary(config_filename)
    return raw_config
