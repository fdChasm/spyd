from cube2common.constants import MAXTEAMLEN
from spyd.registry_manager import register
from spyd.utils.filtertext import filtertext


@register('client_message_handler')
class SetteamHandler(object):
    message_type = 'N_SETTEAM'

    @staticmethod
    def handle(client, room, message):
        team_name = filtertext(message['team'], False, MAXTEAMLEN)
        room.handle_client_event('set_team', client, message['target_cn'], team_name)
