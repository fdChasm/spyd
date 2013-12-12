from cube2common.constants import MAXNAMELEN
from spyd.registry_manager import register
from spyd.utils.filtertext import filtertext


@register('client_message_handler')
class SwitchnameHandler(object):
    message_type = 'N_SWITCHNAME'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(-1)
        name = filtertext(message['name'], False, MAXNAMELEN)
        if len(name) <= 0:
            name = "unnamed"
        room.handle_player_event('switch_name', player, name)
