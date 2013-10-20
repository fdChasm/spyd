from zope.interface import implements

from spyd.authentication.interfaces import IGroupProvider, IAuthSuccess


def domain_to_auth_group(domain):
    ns_parts = domain.split('.')
    ns_parts.reverse()
    ns_parts.append('auth')
    return '.'.join(ns_parts)

class VanillaAuthSuccess(object):
    implements(IAuthSuccess)
    
    def __init__(self, auth_domain, auth_name):
        self.group_provider = VanillaGroupProvider(auth_domain, auth_name)
        self.room_message = "{name#client} claimed auth as {auth#auth_name}@{domain#auth_domain}"
        self.room_message_kwargs = {'auth_name': auth_name, 'auth_domain': auth_domain}
        self.client_message = None
        self.client_message_kwargs = {}

class VanillaGroupProvider(object):
    implements(IGroupProvider)

    def __init__(self, domain, auth_name):
        self.domain = domain
        self.auth_name = auth_name

        self._group_names = (domain_to_auth_group(domain),)

    def get_group_names(self):
        return self._group_names

    def __repr__(self):
        return "<{authentication.auth_name}@{authentication.domain}>".format(authentication=self)
