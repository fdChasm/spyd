from cube2common.utils.enum import enum
from spyd.server.extension.exceptions import AuthenticationHardFailure
import cube2crypto
from spyd.registry_manager import register
import traceback

states = enum('PENDING_CONNECT', 'PENDING_ANSWER', 'AUTHENTICATED', 'DENIED')

@register('gep_authentication_controller', 'cube2crypto')
class Cube2CryptoAuthenticationController(object):
    def __init__(self, config, protocol):
        self._config = config
        self._protocol = protocol
        self._credentials = config.get('credentials')
        self._state = states.PENDING_CONNECT

        self._domain = None
        self._username = None
        self._answer = None
        self._credentials_entry = None
        self._expected_answer = None

    def send(self, message, respid=None):
        if respid is not None:
            message['respid'] = respid
        self._protocol.send(message)

    @property
    def is_authenticated(self):
        return self._state == states.AUTHENTICATED

    @property
    def _is_denied(self):
        return self._state == states.DENIED

    @property
    def groups(self):
        if self._credentials_entry is None: return ()
        if not self.is_authenticated: return ()
        return self._credentials_entry.get('groups', [])

    @property
    def _next_expected_message(self):
        if self._state == states.PENDING_CONNECT:
            return u'connect'
        elif self._state == states.PENDING_ANSWER:
            return u'answer'

    def _issue_challenge(self, domain, username, reqid):
        self._domain = domain
        self._username = username

        self._credentials_entry = self._credentials.get(self._domain, {}).get(self._username)

        public_key = self._credentials_entry['pubkey']

        challenge, self._expected_answer = map(str, cube2crypto.generate_challenge(public_key))

        self.send({"msgtype": "challenge", "challenge": challenge}, respid=reqid)

        self._state = states.PENDING_ANSWER

    def _validate_answer(self, answer, reqid):
        self._answer = answer

        if self._answer == self._expected_answer:
            self.send({"msgtype": "status", "status": "success"}, respid=reqid)
            self._state = states.AUTHENTICATED
        else:
            raise AuthenticationHardFailure()

    def receive(self, message):
        try:
            if self._is_denied: raise AuthenticationHardFailure()

            msg_type = message.get('msgtype')
            if self._next_expected_message != msg_type: raise AuthenticationHardFailure()

            if msg_type == u'connect':
                self._issue_challenge(message.get('domain'), message.get('username'), message.get('reqid', None))
            elif msg_type == u'answer':
                self._validate_answer(message.get('answer'), message.get('reqid', None))
            else:
                raise AuthenticationHardFailure()
        except:
            self._state = states.DENIED
            # traceback.print_exc()
            raise AuthenticationHardFailure()
