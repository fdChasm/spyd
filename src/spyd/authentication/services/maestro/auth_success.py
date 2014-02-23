from zope.interface import implements

from spyd.authentication.interfaces import IGroupProvider, IAuthSuccess
from spyd.authentication.domain_to_auth_group import domain_to_auth_group


class MaestroAuthSuccess(object):
    implements(IAuthSuccess)
    
    def __init__(self, auth_domain, auth_name, uid, groups):
        self.group_provider = MaestroGroupProvider(auth_domain, auth_name, groups)
        self.room_message = "{name#client} claimed auth as {auth#auth_name}@{domain#auth_domain}"
        self.room_message_kwargs = {'auth_name': auth_name, 'auth_domain': auth_domain}
        self.client_message = None
        self.client_message_kwargs = {}

class MaestroGroupProvider(object):
    implements(IGroupProvider)

    def __init__(self, domain, auth_name, groups):
        self.domain = domain
        self.auth_name = auth_name
        self._group_names = groups
        self._group_names.extend([domain_to_auth_group(domain), "{self.auth_name}@{self.domain}".format(self=self)])

    def get_group_names(self):
        return self._group_names

    def __repr__(self):
        return "<MaestroAuthSuccess {authentication.auth_name}@{authentication.domain}>".format(authentication=self)
