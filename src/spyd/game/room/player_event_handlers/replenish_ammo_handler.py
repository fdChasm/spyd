from spyd.registry_manager import register


@register('room_player_event_handler')
class ReplenishAmmoHandler(object):
    event_type = 'replenish_ammo'

    @staticmethod
    def handle(room, player):
        pass
