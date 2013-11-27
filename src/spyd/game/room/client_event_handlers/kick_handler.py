from spyd.registry_manager import register

@register('room_client_event_handler')
class KickHandler(object):
    event_type = 'kick'

    @staticmethod
    def handle(room, client, target_pn, reason):
        # TODO: Implement kicking of players and insertion of bans
        pass

