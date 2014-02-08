from spyd.game.client.exceptions import GenericError


class CommandBase(object):
    @classmethod
    def handles(cls, room, client, command_string):
        'Return whether this command exactly handles the specified command string.'
        return cls.name == command_string

    @classmethod
    def get_handles_fuzzy_score(cls, room, client, command_string):
        'Return a command score object or None if the command cannot be handled.'
        return None

    @classmethod
    def execute(cls, spyd_server, room, client, command_string, arguments):
        'Actually run the command.'
        raise GenericError('Not Implemented.')
