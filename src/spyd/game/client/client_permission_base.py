from spyd.game.client.room_group_provider import RoomGroupProvider
from cube2common.constants import privileges

class ClientPermissionBase(object):
    def __init__(self, permission_resolver):
        self._permission_resolver = permission_resolver
        self._group_name_providers = []

        self._group_name_providers.append(RoomGroupProvider(self))
        
    @property
    def room_privilege(self):
        group_names = self.get_group_names()
        if 'local.room.admin' in group_names:
            return privileges.PRIV_ADMIN
        if 'local.room.auth' in group_names:
            return privileges.PRIV_AUTH
        if 'local.room.master' in group_names:
            return privileges.PRIV_MASTER
        return privileges.PRIV_NONE

    def add_group_name_provider(self, group_name_provider):
        self._group_name_providers.append(group_name_provider)

    def get_group_names(self):
        group_names = set()
        for group_name_provider in self._group_name_providers:
            group_names.update(group_name_provider.get_group_names())
        return group_names

    def allowed(self, functionality):
        group_names = self.get_group_names()
        return self._permission_resolver.groups_allow(group_names, functionality)
