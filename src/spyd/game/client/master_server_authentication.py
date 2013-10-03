class MasterServerAuthentication(object):
    def __init__(self, domain, auth_name):
        self.domain = domain
        self.auth_name = auth_name
        
        print self
        
    def __repr__(self):
        return "<{authentication.auth_name}@{authentication.domain}>".format(authentication=self)