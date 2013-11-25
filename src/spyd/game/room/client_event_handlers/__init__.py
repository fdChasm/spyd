from cube2common.constants import mastermodes
from spyd.game.client.exceptions import UnknownPlayer, InsufficientPermissions, GenericError, StateError
from spyd.game.gamemode import get_mode_name_from_num
from spyd.game.server_message_formatter import info
from spyd.permissions.functionality import Functionality
from spyd.registry_manager import register
from spyd.utils.match_fuzzy import match_fuzzy


@register('room_client_event_handler')
class set_masterHandler(object):
    event_type = 'set_master'

    @staticmethod
    def handle(room, client, target_cn, password_hash, requested_privilege):
        target = room.get_client(target_cn)
        if target is None:
            raise UnknownPlayer(cn=target_cn)

        room._client_try_set_privilege(client, target, requested_privilege)

temporary_set_mastermode_functionality = Functionality("spyd.game.room.temporary.set_mastermode")
set_mastermode_functionality = Functionality("spyd.game.room.set_mastermode")

@register('room_client_event_handler')
class set_master_modeHandler(object):
    event_type = 'set_master_mode'

    @staticmethod
    def handle(room, client, mastermode):
        allowed_set_mastermode = client.allowed(set_mastermode_functionality) or (room.temporary and client.allowed(temporary_set_mastermode_functionality))

        if not allowed_set_mastermode:
            raise InsufficientPermissions('Insufficient permissions to change mastermode.')

        if mastermode < mastermodes.MM_OPEN or mastermode > mastermodes.MM_PRIVATE:
            raise GenericError("Mastermode out of allowed range.")

        room.set_mastermode(mastermode)

set_others_teams_functionality = Functionality("spyd.game.room.set_others_teams", 'Insufficient permissions to change other players teams.')

@register('room_client_event_handler')
class set_teamHandler(object):
    event_type = 'set_team'

    @staticmethod
    def handle(room, client, target_pn, team_name):
        if not client.allowed(set_others_teams_functionality):
            raise InsufficientPermissions(set_others_teams_functionality.denied_message)

        player = room.get_player(target_pn)
        if player is None:
            raise UnknownPlayer(cn=target_pn)

        room.gamemode.on_player_try_set_team(client.get_player(), player, player.team.name, team_name)

set_spectator_functionality = Functionality("spyd.game.room.set_spectator", 'Insufficient permissions to change your spectator status.')
set_other_spectator_functionality = Functionality("spyd.game.room.set_other_spectator", 'Insufficient permissions to change who is spectating.')
set_room_not_spectator_locked_functionality = Functionality("spyd.game.room.set_other_spectator", 'Insufficient permissions to unspectate when mastermode is locked.')

@register('room_client_event_handler')
class set_spectatorHandler(object):
    event_type = 'set_spectator'

    @staticmethod
    def handle(room, client, target_pn, spectate):
        player = room.get_player(target_pn)
        if player is None:
            raise UnknownPlayer(cn=target_pn)

        if client.get_player() is player:
            if not client.allowed(set_spectator_functionality):
                raise InsufficientPermissions(set_spectator_functionality.denied_message)
            if not spectate and not client.allowed(set_room_not_spectator_locked_functionality):
                raise InsufficientPermissions(set_room_not_spectator_locked_functionality.denied_message)
        else:
            if not client.allowed(set_other_spectator_functionality):
                raise InsufficientPermissions(set_other_spectator_functionality.denied_message)

        room._set_player_spectator(player, spectate)

@register('room_client_event_handler')
class kickHandler(object):
    event_type = 'kick'

    @staticmethod
    def handle(room, client, target_pn, reason):
        # TODO: Implement kicking of players and insertion of bans
        pass

@register('room_client_event_handler')
class clear_bansHandler(object):
    event_type = 'clear_bans'

    @staticmethod
    def handle(room, client):
        # TODO: Implement clearing of bans
        pass

set_map_mode_functionality = Functionality("spyd.game.room.set_map_mode", 'Insufficient permissions to force a map/mode change.')

@register('room_client_event_handler')
class map_voteHandler(object):
    event_type = 'map_vote'

    @staticmethod
    def handle(room, client, map_name, mode_num):
        if not client.allowed(set_map_mode_functionality):
            raise InsufficientPermissions(set_map_mode_functionality.denied_message)

        mode_name = get_mode_name_from_num(mode_num)
        valid_map_names = room._map_mode_state.get_map_names()
        map_name_match = match_fuzzy(map_name, valid_map_names)
        if map_name_match is None:
            raise GenericError('Could not resolve map name to valid map. Please try again.')
        room.change_map_mode(map_name_match, mode_name)

@register('room_client_event_handler')
class map_crcHandler(object):
    event_type = 'map_crc'

    @staticmethod
    def handle(room, client, crc):
        # TODO: Implement optional spectating of clients without valid map CRC's
        pass

@register('room_client_event_handler')
class item_listHandler(object):
    event_type = 'item_list'

    @staticmethod
    def handle(room, client, item_list):
        room.gamemode.on_client_item_list(client, item_list)

@register('room_client_event_handler')
class base_listHandler(object):
    event_type = 'base_list'

    @staticmethod
    def handle(room, client, base_list):
        room.gamemode.on_client_base_list(client, base_list)

@register('room_client_event_handler')
class flag_listHandler(object):
    event_type = 'flag_list'

    @staticmethod
    def handle(room, client, flag_list):
        room.gamemode.on_client_flag_list(client, flag_list)

pause_resume_functionality = Functionality("spyd.game.room.pause_resume", 'Insufficient permissions to pause or resume the game.')

@register('room_client_event_handler')
class pause_gameHandler(object):
    event_type = 'pause_game'

    @staticmethod
    def handle(room, client, pause):
        if not client.allowed(pause_resume_functionality):
            raise InsufficientPermissions(pause_resume_functionality.denied_message)

        if pause:
            if room.is_paused and not room.is_resuming: raise StateError('The game is already paused.')
            room.pause()
            room._broadcaster.server_message(info("{name#client} has paused the game.", client=client))
        elif not pause:
            if not room.is_paused: raise StateError('The game is already resumed.')
            room.resume()
            room._broadcaster.server_message(info("{name#client} has resumed the game.", client=client))

@register('room_client_event_handler')
class set_demo_recordingHandler(object):
    event_type = 'set_demo_recording'

    @staticmethod
    def handle(room, client, value):
        pass

@register('room_client_event_handler')
class stop_demo_recordingHandler(object):
    event_type = 'stop_demo_recording'

    @staticmethod
    def handle(room, client):
        pass

@register('room_client_event_handler')
class clear_demoHandler(object):
    event_type = 'clear_demo'

    @staticmethod
    def handle(room, client, demo_id):
        pass

@register('room_client_event_handler')
class list_demosHandler(object):
    event_type = 'list_demos'

    @staticmethod
    def handle(room, client):
        pass

@register('room_client_event_handler')
class get_demoHandler(object):
    event_type = 'get_demo'

    @staticmethod
    def handle(room, client, demo_id):
        pass

@register('room_client_event_handler')
class add_botHandler(object):
    event_type = 'add_bot'

    @staticmethod
    def handle(room, client, skill):
        pass

@register('room_client_event_handler')
class delete_botHandler(object):
    event_type = 'delete_bot'

    @staticmethod
    def handle(room, client):
        pass

@register('room_client_event_handler')
class set_bot_balanceHandler(object):
    event_type = 'set_bot_balance'

    @staticmethod
    def handle(room, client, balance):
        pass

@register('room_client_event_handler')
class set_bot_limitHandler(object):
    event_type = 'set_bot_limit'

    @staticmethod
    def handle(room, client, limit):
        pass

@register('room_client_event_handler')
class check_mapsHandler(object):
    event_type = 'check_maps'

    @staticmethod
    def handle(room, client):
        pass

@register('room_client_event_handler')
class set_game_speedHandler(object):
    event_type = 'set_game_speed'

    @staticmethod
    def handle(room, client, speed):
        pass

@register('room_client_event_handler')
class edit_get_mapHandler(object):
    event_type = 'edit_get_map'

    @staticmethod
    def handle(room, client):
        pass

@register('room_client_event_handler')
class edit_new_mapHandler(object):
    event_type = 'edit_new_map'

    @staticmethod
    def handle(room, client, size):
        pass

@register('room_client_event_handler')
class edit_remipHandler(object):
    event_type = 'edit_remip'

    @staticmethod
    def handle(room, client):
        pass

@register('room_client_event_handler')
class commandHandler(object):
    event_type = 'command'

    @staticmethod
    def handle(room, client, command):
        pass

