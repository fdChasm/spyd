from twisted.python import usage

class Options(usage.Options):
    optParameters = [
        ['homedir',     'h', './',                  'The directory to switch to and run from.'],
        ['bindingpath', 'b', './bin/spyd_binding',  'The path to use for the spyd_binding executable.'],
        ['config',      'c', 'config.json',         'The config file to use.'],
    ]
