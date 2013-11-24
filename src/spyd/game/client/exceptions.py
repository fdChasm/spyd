from spyd.game.server_message_formatter import smf

class InvalidPlayerNumberReference(Exception): pass

class GenericError(Exception):
    def __init__(self, message_fmt, *fmt_args, **fmt_kwargs):
        self.message = smf.vformat(message_fmt, fmt_args, fmt_kwargs)

class StateError(GenericError): pass
class UsageError(GenericError): pass
class InsufficientPermissions(GenericError): pass
class UnknownPlayer(GenericError):
    def __init__(self, cn=None, name=None):
        if cn is not None:
            message_fmt = 'No player with cn {cn#cn} found.'
            fmt_kwargs = {'cn': cn}
        elif name is not None:
            message_fmt = 'Could not resolve name {name#name} to a player.'
            fmt_kwargs = {'name': name}
        else:
            message_fmt = 'Unknown player.'
            fmt_kwargs = {}
        GenericError.__init__(self, message_fmt, **fmt_kwargs)
