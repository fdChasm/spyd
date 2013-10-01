config = {
    'lan_findable': True,
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
    }
}