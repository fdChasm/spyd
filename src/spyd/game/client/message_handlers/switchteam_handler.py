from cube2common.constants import MAXTEAMLEN
from spyd.registry_manager import register
from spyd.utils.filtertext import filtertext


@register('client_message_handler')
class SwitchteamHandler(object):
    message_type = 'N_SWITCHTEAM'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(-1)
        team_name = filtertext(message['team'], False, MAXTEAMLEN)
        room.handle_player_event('switch_team', player, team_name)
