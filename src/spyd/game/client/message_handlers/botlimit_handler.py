from spyd.registry_manager import register


@register('client_message_handler')
class BotlimitHandler(object):
    message_type = 'N_BOTLIMIT'

    @staticmethod
    def handle(client, room, message):
        room.handle_client_event('set_bot_limit', client, message['limit'])
