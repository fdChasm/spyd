from spyd.game.client.exceptions import UnknownPlayer
from spyd.registry_manager import register


@register('room_client_event_handler')
class SetMasterHandler(object):
    event_type = 'set_master'

    @staticmethod
    def handle(room, client, target_cn, password_hash, requested_privilege):
        target = room.get_client(target_cn)
        if target is None:
            raise UnknownPlayer(cn=target_cn)

        room._client_try_set_privilege(client, target, requested_privilege)
