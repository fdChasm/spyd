import re

from spyd.game.client.client_message_handling_base import GenericError, InsufficientPermissions
import spyd.game.command.commands # @UnusedImport
from spyd.game.command.command_finder import CommandFinder
import shlex


command_pattern = re.compile("^#(?P<command_string>[\w-]+)(\s(?P<arg_string>.*))?$")

class CommandExecuter(object):
    def __init__(self):
        self._command_finder = CommandFinder()

    def execute(self, room, client, command_string):
        command_match = command_pattern.match(command_string)
        
        if command_match is None:
            raise GenericError("Invalid command input.")
        
        command_string = command_match.group('command_string')
        arg_string = command_match.group('arg_string') or ""
        
        if command_string is None:
            raise GenericError("Invalid command input.")
        
        command_handler = self._command_finder.find(room, client, command_string)
        
        if command_handler is None:
            raise GenericError("Unknown command.")
        
        execute_functionality = command_handler.functionality
        
        if not client.allowed(execute_functionality):
            raise InsufficientPermissions(execute_functionality.denied_message)

        try:
            args = shlex.split(arg_string)
        except ValueError, e:
            raise GenericError("Invalid input: {error}", error=e.message)
        
        command_handler.execute(room, client, command_string, args)
