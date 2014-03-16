from twisted.internet import defer

from spyd.game.client.exceptions import GenericError
from spyd.utils.match_fuzzy import match_fuzzy


@defer.inlineCallbacks
def resolve_map_name(room, map_name):
    valid_map_names = yield room.get_map_names()
    map_name_match = match_fuzzy(unicode(map_name, 'utf_8'), valid_map_names)

    if map_name_match is None:
        raise GenericError('Could not resolve map name {value#map_name} to valid map. Please try again.', map_name=map_name)

    defer.returnValue(map_name_match)
