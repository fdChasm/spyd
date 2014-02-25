import spyd.game.command.commands  # @UnusedImport
from spyd.registry_manager import RegistryManager


class CommandFinder(object):
    def __init__(self):
        self.command_handlers = set()
        for registered_command in RegistryManager.get_registrations('command'):
            self.command_handlers.add(registered_command.registered_object)
    
    def _find_fuzzy(self, room, client, command_string):
        command_scores = map(lambda ch: ch.get_handles_fuzzy_score(room, client, command_string), self.command_handlers)
        command_scores = filter(None, command_scores)
        
        if not command_scores:
            return None
        
        best_matching_command_score = max(command_scores, key=lambda command_score: command_score.score)
        
        return best_matching_command_score.command_handler
    
    def find(self, room, client, command_string):
        for command_handler in self.command_handlers:
            if command_handler.handles(room, client, command_string):
                return command_handler
        return self._find_fuzzy(room, client, command_string)

    def get_command_list(self):
        return list(self.command_handlers)
