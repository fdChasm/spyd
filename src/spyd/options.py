from twisted.python import usage

class Options(usage.Options):
    optParameters = [
        ['servdir',     's', './',                  'The directory to switch to and run from.']
    ]
    optFlags = [
        ["init", "i", "Initialize the server specified servdir with the default config files."]
    ]
