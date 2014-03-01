import Levenshtein

def match_fuzzy(identifier, possibility_list, allow_ci_check=True):
        "Returns the nearest match to the text of identifier from a list of possibilities."
        if not len(possibility_list): return None
        threshold = len(identifier) - 1

        closest_match = min(possibility_list, key=lambda m: Levenshtein.distance(m, identifier))
        distance = Levenshtein.distance(closest_match, identifier)

        if distance <= threshold: return closest_match

        if not allow_ci_check: return None

        identifier = identifier.lower()

        closest_match = min(possibility_list, key=lambda m: Levenshtein.distance(m.lower(), identifier))
        distance = Levenshtein.distance(closest_match.lower(), identifier)

        if distance <= threshold: return closest_match

        return None
