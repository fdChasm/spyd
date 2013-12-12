from spyd.registry_manager import register


@register('client_message_handler')
class ItempickupHandler(object):
    message_type = 'N_ITEMPICKUP'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('pickup_item', player, message['item_index'])
