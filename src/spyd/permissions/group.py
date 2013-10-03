class GroupAllowsDeniesIntersection(Exception): pass


class Group(object):
    def __init__(self, name, inherits, priority, allows, denies):
        self.name = name
        # groups this group inherits from
        self._inherits = inherits
        # group names or group name patterns this group overrides
        self.priority = priority
        # allowed functionality names
        self._allows = allows
        # denied functionality names
        self._denies = denies

    def allowed(self, functionality_name):
        'Returns True, None, or False'
        if self._search_is_denied(functionality_name):
            return False
        if self._search_is_allowed(functionality_name):
            return True

        inherited_allows = map(lambda g: g.allowed(functionality_name), self._inherits)
        
        # Filter out None from the inherited _allows because they shouldn't count as _denies
        inherited_allows = filter(lambda a: a is not None, inherited_allows)

        if len(inherited_allows) == 0:
            return None

        inherited_allow = all(inherited_allows)

        return inherited_allow

    def _search_is_allowed(self, functionality_name):
        for allow in self._allows:
            if allow.match(functionality_name):
                return True
        return False

    def _search_is_denied(self, functionality_name):
        for deny in self._denies:
            if deny.match(functionality_name):
                return True
        return False
