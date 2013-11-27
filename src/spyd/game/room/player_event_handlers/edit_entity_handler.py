from spyd.registry_manager import register


@register('room_player_event_handler')
class EditEntityHandler(object):
    event_type = 'edit_entity'

    @staticmethod
    def handle(room, player, entity_id, entity_type, x, y, z, attrs):
        pass
