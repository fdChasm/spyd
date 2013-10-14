from twisted.python import usage

class Options(usage.Options):
    optParameters = [
        ['homedir',     'h', './',                  'The directory to switch to and run from.'],
        ['config',      'c', 'config.json',         'The config file to use.'],
    ]
