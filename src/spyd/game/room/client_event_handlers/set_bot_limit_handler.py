from spyd.registry_manager import register

@register('room_client_event_handler')
class SetBotLimitHandler(object):
    event_type = 'set_bot_limit'

    @staticmethod
    def handle(room, client, limit):
        pass

