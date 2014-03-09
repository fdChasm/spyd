import time

from spyd.punitive_effects.punitive_effect_info import TimedExpiryInfo, EffectInfo
from spyd.registry_manager import register
from cube2common.constants import disconnect_types
from spyd.game.server_message_formatter import error


SECONDS_PER_HOUR = 60 * 60

@register('room_client_event_handler')
class KickHandler(object):
    event_type = 'kick'

    @staticmethod
    def handle(room, client, target_pn, reason):
        # TODO: Permissions checks

        print client, target_pn, reason

        target_client = room.get_client(target_pn)

        expiry_time = time.time() + (4 * SECONDS_PER_HOUR)

        client._punitive_model.add_effect('ban', target_client.host, EffectInfo(TimedExpiryInfo(expiry_time)))

        target_client.disconnect(disconnect_types.DISC_KICK, error("You were kicked by {name#kicker}", kicker=target_client))
