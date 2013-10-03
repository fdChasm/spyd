class ClientPermissionBase(object):
    def __init__(self, permission_resolver):
        self._permission_resolver = permission_resolver
        self._group_name_providers = []

    def add_group_name_provider(self, group_name_provider):
        self._group_name_providers.append(group_name_provider)

    def get_group_names(self):
        group_names = []
        for group_name_provider in self._group_name_providers:
            group_names.extend(group_name_provider.get_group_names)
        return group_names

    def allowed(self, functionality):
        group_names = self.get_group_names()
        return self._permission_resolver.groups_allow(group_names, functionality)
