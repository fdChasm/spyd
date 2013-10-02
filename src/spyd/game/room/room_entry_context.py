class RoomEntryContext(object):
    def __init__(self, client, authentication, pwdhash):
        self.client = client
        self.authentication = authentication
        self.pwdhash = pwdhash