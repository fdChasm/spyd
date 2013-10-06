from spyd.game.server_message_formatter import smf
class Functionality(object):
    def __init__(self, name, denied_message=None, *message_values, **message_fields):
        self.name = name
        
        msg_fmt = denied_message or "Not allowed."
        self.denied_message = smf.vformat(msg_fmt, message_values, message_fields)
        
    def __repr__(self):
        return "<Functionality: {!r}>".format(self.name)
