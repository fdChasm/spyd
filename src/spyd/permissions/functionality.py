class Functionality(object):
    def __init__(self, name, denied_message=None):
        self.name = name
        self.denied_message = denied_message or "Not allowed."
        
    def __repr__(self):
        return "<Functionality: {!r}>".format(self.name)
