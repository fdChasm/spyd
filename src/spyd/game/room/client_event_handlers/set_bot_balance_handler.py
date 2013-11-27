from spyd.registry_manager import register

@register('room_client_event_handler')
class SetBotBalanceHandler(object):
    event_type = 'set_bot_balance'

    @staticmethod
    def handle(room, client, balance):
        pass

