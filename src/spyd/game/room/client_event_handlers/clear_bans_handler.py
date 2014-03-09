from spyd.registry_manager import register


@register('room_client_event_handler')
class ClearBansHandler(object):
    event_type = 'clear_bans'

    @staticmethod
    def handle(room, client):
        # TODO: Permissions checks
        client._punitive_model.clear_effects('ban')
