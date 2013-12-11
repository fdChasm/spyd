from spyd.game.player.player import Player
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register


@register('gep_message_handler')
class SpydGetPlayerInfoMessageHandler(object):
    msgtype = 'get_player_info'
    execute = Functionality(msgtype)

    @classmethod
    def handle_message(cls, spyd_server, gep_client, message):
        player_uuid = message['player']

        player = Player.instances_by_uuid.get(player_uuid, None)

        if player is None:
            raise Exception("Unknown player.")

        state = player.state

        player_game_state = {
            'is_spectator': state.is_spectator,
            'is_alive': state.is_alive,
            'has_quad': state.has_quad,
            'frags': state.frags,
            'deaths': state.deaths,
            'suicides': state.suicides,
            'teamkills': state.teamkills,
            'damage_dealt': state.damage_dealt,
            'damage_spent': state.damage_spent,
            'flags': state.flags,
            'flag_returns': state.flag_returns,
            'health': state.health,
            'maxhealth': state.maxhealth,
            'armour': state.armour,
            'armourtype': state.armourtype,
            'gunselect': state.gunselect,
            'ammo': state.ammo
        }

        player_info = {
            'cn': player.cn,
            'name': player.name,
            'team': player.team_name,
            'room': player.room.name,
            'host': player.client.host,
            'model': player.playermodel,
            'isai': player.isai,
            'groups': tuple(player.client.get_group_names()),
            'game_state': player_game_state
        }

        gep_client.send({'msgtype': 'player_info', 'player': player.uuid, 'player_info': player_info}, message.get('reqid'))
