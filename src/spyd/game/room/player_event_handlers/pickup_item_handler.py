from spyd.registry_manager import register


@register('room_player_event_handler')
class PickupItemHandler(object):
    event_type = 'pickup_item'

    @staticmethod
    def handle(room, player, item_index):
        room.gamemode.on_player_pickup_item(player, item_index)
