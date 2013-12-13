import zope.interface

class IAuthService(zope.interface.Interface):
    def handles_domain(self, auth_domain):
        '''
        Parameters
        ----------
        auth_domain : string
        '''
    
    def try_authenticate(self, auth_domain, auth_name):
        '''
        Parameters
        ----------
        auth_domain : string
            The name of auth domain with which to authenticate.
        auth_name : string
            The auth name to try to authenticate with.

        Returns
        ----------
        Deferred
            Yields IAuthChallenge, errs AuthFailedException
        '''

    def answer_challenge(self, auth_domain, auth_id, answer):
        '''
        Parameters
        ----------
        auth_domain : string
            The name of auth domain with which the client is authenticating.
        auth_id : int
            The auth id of the challenge which the client is answering.
        answer : string
            The answer to the auth challenge.

        Returns
        ----------
        Deferred
            Yields IAuthSuccess, errs AuthFailedException
        '''

class IAuthChallenge(zope.interface.Interface):
    auth_id = zope.interface.Attribute('The auth id of the challenge.')
    auth_domain = zope.interface.Attribute('The name of auth domain with which the client is authenticating.')
    challenge = zope.interface.Attribute('The auth challenge string.')

class IAuthSuccess(zope.interface.Interface):
    group_provider = zope.interface.Attribute('An object providing the IGroupProvider interface.')
    room_message = zope.interface.Attribute('The message to display to the room the client is in.')
    room_message_kwargs = zope.interface.Attribute('Keyword arguments used to populate the room message.')
    client_message = zope.interface.Attribute('The message to display to the client.')
    client_message_kwargs = zope.interface.Attribute('Keyword arguments used to populate the client message.')

class IGroupProvider(zope.interface.Interface):
    def get_group_names(self):
        '''Returns a list of groups.'''
