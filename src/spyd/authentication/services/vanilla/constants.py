from cube2common.utils.enum import enum



authentication_states = enum('PENDING_CHALLENGE', 'PENDING_ANSWER', 'PENDING_RESPONSE')

possible_commands = ('failreg', 'succreg', 'addgban', 'cleargbans', 'chalauth', 'failauth', 'succauth')