'''
**** Form 1 ****

#duel 45
  -> "[FD]Chasm has challenged you to a duel. Type #duel 12 to accept."

#duel 45 ffa
  -> "[FD]Chasm has challenged you to a duel on ffa. Type #duel 12 to accept."

#duel 45 ffa complex
  -> "[FD]Chasm has challenged you to a duel on ffa complex. Type #duel 12 to accept."

**** Form 2 ****

#duel
  -> "[FD]Chasm is looking for a duel. Type #duel 12 to accept."

#duel ffa
  -> "[FD]Chasm is looking for a duel on ffa. Type #duel 12 to accept."

#duel ffa complex
  -> "[FD]Chasm is looking for a duel on ffa complex. Type #duel 12 to accept."

'''

from collections import deque
import re
import traceback

from twisted.internet import defer

from spyd.game.client.exceptions import GenericError
from spyd.game.command.command_base import CommandBase
from spyd.game.gamemode import gamemodes
from spyd.game.map.map_rotation import MapRotation
from spyd.game.map.resolve_map_name import resolve_map_name
from spyd.game.server_message_formatter import info, smf
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.utils.match_fuzzy import match_fuzzy


cn_chall_msg = "{client} has challenged you to a duel{challenge_details}. Type {action#duel_command} to accept."
looking_msg = "{client} is looking for a duel{challenge_details}. Type {action#duel_command} to accept."

chall_sent_msg = "Challenge sent."

duel_command = "duel {client.cn}"

form1 = re.compile(r'(?P<cn>\d+)(\s+(?P<mode_name>\w+)(\s+(?P<map_name>\w+))?)?')
form2 = re.compile(r'((?P<mode_name>\w+)(\s+(?P<map_name>\w+))?)?')

def get_challenge_details(mode_name, map_name):
    "Gets the string describing the map and or mode for the duel challenge."
    if mode_name is not None and map_name is not None:
        return smf.format(" on {value#mode_name} {value#map_name}", mode_name=mode_name, map_name=map_name)
    elif mode_name is not None:
        return smf.format(" on {value#mode_name}", mode_name=mode_name)
    elif map_name is not None:
        return smf.format(" on {value#map_name}", map_name=map_name)
    else:
        return ""

def parse_arguments(raw_args):
    match = form1.search(raw_args)
    if match is None:
        match = form2.search(raw_args)
        if match is None: raise GenericError("No match.")

    args = match.groupdict()

    cn = args.get('cn', None)
    mode_name = args.get('mode_name', None)
    map_name = args.get('map_name', None)

    return cn, mode_name, map_name

class NullChallenge(object):
    @classmethod
    def applies_to_client(cls, client):
        return False

class GeneralChallenge(object):
    def __init__(self, mode_name, map_name):
        self.mode_name = mode_name
        self.map_name = map_name

    def applies_to_client(self, client):
        return True

class SpecificChallenge(object):
    def __init__(self, target, mode_name, map_name):
        self.target = target
        self.mode_name = mode_name
        self.map_name = map_name

    def applies_to_client(self, client):
        return self.target == client

def get_existing_challenge(client, target):
    challenge = getattr(client, 'duel_challenge', NullChallenge)
    if challenge.applies_to_client(target):
        return challenge

def save_specific_challenge(client, target, mode_name, map_name):
    client.duel_challenge = SpecificChallenge(target, mode_name, map_name)

def save_general_challenge(client, mode_name, map_name):
    client.duel_challenge = GeneralChallenge(mode_name, map_name)

def begin_duel(room, client, target, existing_challenge):
    room_name = "{}x{}".format(client.cn, target.cn)
    
    mode_name = existing_challenge.mode_name
    map_name = existing_challenge.map_name

    room_factory = room.manager.room_factory

    if mode_name is None:
        mode_name = "ffa"

    if map_name is None:
        map_name = 'complex'
        

    room_config = room_factory.get_room_config(room_name, 'temporary')
    default_map_rotation = room_config.get('map_rotation', {})

    map_names = default_map_rotation.get('rotations', {}).get(mode_name, deque(['complex']))

    map_rotation = MapRotation.from_dictionary({"rotations": {mode_name: map_names}, "modes": [mode_name]})

    map_rotation.advance_to_map(map_name)

    target_room = room_factory.build_room(room_name, 'temporary', map_rotation)

    target_room.temporary = True

    target_room.masters.add(client)
    target_room.masters.add(target)

    room.manager.client_change_room(client, target_room)
    room.manager.client_change_room(target, target_room)

@register("command")
class DuelCommand(CommandBase):
    name = "duel"
    functionality = Functionality("spyd.game.commands.duel.execute", "You do not have permission to execute {action#command}", command=name)
    usage = "(cn) (mode) (map) | (mode) (map)"
    description = "Indicate you are looking for a duel or challenge a specific player."

    @classmethod
    @defer.inlineCallbacks
    def execute(cls, spyd_server, room, client, command_string, arguments, raw_args):
        try:
            cn, mode_name, map_name = parse_arguments(raw_args)

            if mode_name is not None:
                valid_mode_names = gamemodes.keys()
                mode_name_match = match_fuzzy(str(mode_name), valid_mode_names)

                if mode_name_match is None:
                    raise GenericError('Could not resolve mode name {value#mode_name} to valid mode. Please try again.', mode_name=mode_name)

                mode_name = mode_name_match

            if map_name is not None:
                map_name = yield resolve_map_name(room, map_name)

            duel_command_msg = duel_command.format(client=client)
            challenge_details = get_challenge_details(mode_name, map_name)

            if cn is not None:
                target = room.get_client(int(cn))
                if target is client:
                    raise GenericError("You can't duel yourself.")

                existing_challenge = get_existing_challenge(target, client)

                if existing_challenge is not None:
                    begin_duel(room, client, target, existing_challenge)

                else:
                    save_specific_challenge(client, target, mode_name, map_name)
                    target.send_server_message(info(cn_chall_msg, client=client, challenge_details=challenge_details, duel_command=duel_command_msg))
                    client.send_server_message(info(chall_sent_msg))

            else:
                save_general_challenge(client, mode_name, map_name)
                room.server_message(info(looking_msg, client=client, challenge_details=challenge_details, duel_command=duel_command_msg), exclude=(client,))
                client.send_server_message(info(chall_sent_msg))
        except:
            traceback.print_exc()
