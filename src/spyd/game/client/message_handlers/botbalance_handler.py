from spyd.registry_manager import register


@register('client_message_handler')
class BotbalanceHandler(object):
    message_type = 'N_BOTBALANCE'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('set_bot_balance', client, message['balance'])
