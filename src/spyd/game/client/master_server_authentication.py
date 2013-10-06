def domain_to_auth_group(domain):
    ns_parts = domain.split('.')
    ns_parts.reverse()
    ns_parts.append('auth')
    return '.'.join(ns_parts)

class MasterServerAuthentication(object):
    def __init__(self, domain, auth_name):
        self.domain = domain
        self.auth_name = auth_name
        
        self._group_names = ( domain_to_auth_group(domain), )
        
    def get_group_names(self):
        return self._group_names
        
    def __repr__(self):
        return "<{authentication.auth_name}@{authentication.domain}>".format(authentication=self)