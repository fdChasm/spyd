from twisted.internet import defer

from spyd.game.server_message_formatter import error, info
from spyd.protocol import swh


class ClientAuthState(object):
    def __init__(self, client, auth_world_view):
        self.client = client
        self.auth_world_view = auth_world_view

        self.auth_deferred = None

    def auth(self, authdomain, authname):
        if self.auth_deferred is not None:
            self.client.send_server_message(error("You already have a pending auth request wait for the previous one to complete."))
            return defer.fail(None)

        auth_deferred = defer.Deferred()
        self.auth_deferred = auth_deferred

        deferred = self.auth_world_view.try_authenticate(authdomain, authname)

        deferred.addCallback(self.on_auth_challenge)
        deferred.addErrback(self.on_auth_failure)

        return auth_deferred

    def answer_auth_challenge(self, authdomain, authid, answer):
        if self.auth_deferred is None:
            return

        deferred = self.auth_world_view.answer_challenge(authdomain, authid, answer)

        deferred.addCallback(self.on_auth_success)
        deferred.addErrback(self.on_auth_failure)

    def on_auth_challenge(self, auth_challenge):
        auth_id = auth_challenge.auth_id
        auth_domain = auth_challenge.auth_domain
        challenge = auth_challenge.challenge

        with self.client.sendbuffer(1, True) as cds:
            swh.put_authchall(cds, auth_domain, auth_id, challenge)

    def on_auth_failure(self, deferred_exception):
        self.client.send_server_message(error(deferred_exception.value.message))
        self.auth_deferred.errback(deferred_exception)
        self.auth_deferred = None

    def on_auth_success(self, auth_success):
        if auth_success is not None:
            self.client.add_group_name_provider(auth_success.group_provider)

            if auth_success.room_message is not None and self.client.connection_sequence_complete:
                auth_success.room_message_kwargs['client'] = self.client
                self.client.room._broadcaster.server_message(info(auth_success.room_message, **auth_success.room_message_kwargs))

        self.auth_deferred.callback(auth_success)
        self.auth_deferred = None
