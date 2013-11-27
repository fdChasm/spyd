from spyd.registry_manager import register

@register('room_client_event_handler')
class SetGameSpeedHandler(object):
    event_type = 'set_game_speed'

    @staticmethod
    def handle(room, client, speed):
        pass

