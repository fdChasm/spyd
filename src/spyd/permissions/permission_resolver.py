import re
import string

from spyd.permissions.group import Group


class GroupInheritanceCycle(Exception): pass
class MissingGroup(Exception): pass
class MissingInheritedGroup(Exception): pass


def create_simple_pattern(pattern_string):
    "Takes a group or functionality pattern string and converts it into a RegexObject."
    pattern_string = string.replace(pattern_string, '.', '\.')
    pattern_string = string.replace(pattern_string, '*', '.*')
    pattern_string = "^{}$".format(pattern_string)
    return re.compile(pattern_string)

class PermissionResolver(object):
    def __init__(self):
        # group: Group
        self.groups = {}

    def groups_allow(self, group_name_list, functionality):
        groups = self._group_names_to_groups(group_name_list)
        groups = filter(None, groups)
        
        allowed_results = map(lambda g: (g.priority, g.allowed(functionality.name)), groups)
        allowed_results = filter(lambda gar: gar[1] is not None, allowed_results)
        
        allow_results = filter(lambda gar: gar[1], allowed_results)
        deny_results = filter(lambda gar: not gar[1], allowed_results)
        
        if not allow_results: return False
        if not deny_results: return True
        
        max_allow_result_priority = max(allow_results, key=lambda gar: gar[0])[0]
        max_deny_result_priority = max(deny_results, key=lambda gar: gar[0])[0]
        
        return max_allow_result_priority > max_deny_result_priority
        
    def _group_names_to_groups(self, group_name_list):
        return map(lambda gn: self.groups.get(gn, None), group_name_list)

    @staticmethod
    def from_dictionary(permission_dictionary):
        permission_resolver = PermissionResolver()

        groups = permission_resolver.groups

        def create_group(group_name, inheritance_path):
            if group_name in groups: return groups[group_name]
            if group_name in inheritance_path:
                raise GroupInheritanceCycle()

            inheritance_path.add(group_name)

            group_data = permission_dictionary.get(group_name, None)
            if group_data is None:
                raise MissingGroup()

            group_inherits = set()
            for inherits_group_name in group_data.get('inherits', ()):
                try:
                    group = create_group(inherits_group_name, inheritance_path.copy())
                except MissingGroup:
                    raise MissingInheritedGroup("{group} inherits from {inherits_group!r} but {inherits_group!r} was not declared.".format(group=group_name, inherits_group=inherits_group_name))
                group_inherits.add(group)

            group_allows = map(create_simple_pattern, group_data.get('allows', ()))
            group_denies = map(create_simple_pattern, group_data.get('denies', ()))
            group_priority = group_data.get('priority', None)
            group = Group(group_name, group_inherits, group_priority, group_allows, group_denies)
            groups[group_name] = group
            return group

        for group_name in permission_dictionary:
            create_group(group_name, set())

        return permission_resolver
