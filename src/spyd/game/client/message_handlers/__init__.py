from spyd.registry_manager import register

from cube2common.constants import disconnect_types, MAXNAMELEN, MAXTEAMLEN
from cube2common.vec import vec
from spyd.game.edit.selection import Selection
from spyd.protocol import swh
from spyd.utils.dictionary_get import dictget
from spyd.utils.filtertext import filtertext


@register('client_message_handler')
class ConnectHandler(object):
    message_type = 'N_CONNECT'

    @staticmethod
    def handle(client, room, message):
        if not client.is_connected:
            client.connect_received(message)


@register('client_message_handler')
class PingHandler(object):
    message_type = 'N_PING'

    @staticmethod
    def handle(client, room, message):
        with client.sendbuffer(1, False) as cds:
            swh.put_pong(cds, message['cmillis'])


@register('client_message_handler')
class PosHandler(object):
    message_type = 'N_POS'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['clientnum'])
        player.state.update_position(message['position'], message['raw_position'])


@register('client_message_handler')
class ClientpingHandler(object):
    message_type = 'N_CLIENTPING'

    @staticmethod
    def handle(client, room, message):
        ping = message['ping']
        client.ping_buffer.add(ping)
        player = client.get_player()
        swh.put_clientping(player.state.messages, ping)


@register('client_message_handler')
class SoundHandler(object):
    message_type = 'N_SOUND'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_sound(player, message['sound'])


@register('client_message_handler')
class SpawnHandler(object):
    message_type = 'N_SPAWN'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_spawn(player, message['lifesequence'], message['gunselect'])


@register('client_message_handler')
class SwitchmodelHandler(object):
    message_type = 'N_SWITCHMODEL'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_switch_model(player, message['playermodel'])


@register('client_message_handler')
class SwitchnameHandler(object):
    message_type = 'N_SWITCHNAME'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(-1)
        name = filtertext(message['name'], False, MAXNAMELEN)
        if len(name) <= 0:
            name = "unnamed"
        room.on_player_switch_name(player, name)


@register('client_message_handler')
class SwitchteamHandler(object):
    message_type = 'N_SWITCHTEAM'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(-1)
        team_name = filtertext(message['team'], False, MAXTEAMLEN)
        room.on_player_switch_team(player, team_name)


@register('client_message_handler')
class SetteamHandler(object):
    message_type = 'N_SETTEAM'

    @staticmethod
    def handle(client, room, message):
        team_name = filtertext(message['team'], False, MAXTEAMLEN)
        room.on_client_set_team(client, message['target_cn'], team_name)


@register('client_message_handler')
class SpectatorHandler(object):
    message_type = 'N_SPECTATOR'

    @staticmethod
    def handle(client, room, message):
        room.on_client_set_spectator(client, message['target_cn'], bool(message['value']))


@register('client_message_handler')
class MapvoteHandler(object):
    message_type = 'N_MAPVOTE'

    @staticmethod
    def handle(client, room, message):
        room.on_client_map_vote(client, message['map_name'], message['mode_num'])


@register('client_message_handler')
class MapchangeHandler(object):
    message_type = 'N_MAPCHANGE'

    @staticmethod
    def handle(client, room, message):
        room.on_client_map_vote(client, message['map_name'], message['mode_num'])


@register('client_message_handler')
class MapcrcHandler(object):
    message_type = 'N_MAPCRC'

    @staticmethod
    def handle(client, room, message):
        room.on_client_map_crc(client, message['mapcrc'])


@register('client_message_handler')
class AuthansHandler(object):
    message_type = 'N_AUTHANS'

    @staticmethod
    def handle(client, room, message):
        authdomain = message['authdomain']
        authid = message['authid']
        answer = message['answer']
        client.answer_auth_challenge(authdomain, authid, answer)


@register('client_message_handler')
class AuthtryHandler(object):
    message_type = 'N_AUTHTRY'

    @staticmethod
    def handle(client, room, message):
        authdomain = message['authdomain']
        authname = message['authname']

        deferred = client.auth(authdomain, authname)


@register('client_message_handler')
class AuthkickHandler(object):
    message_type = 'N_AUTHKICK'

    @staticmethod
    def handle(client, room, message):
        authdomain = message['authdomain']
        authname = message['authname']
        target_pn = message['target_cn']
        reason = message['reason']

        deferred = client.auth(authdomain, authname)
        deferred.addCallback(lambda a: room.on_client_kick(client, target_pn, reason))


@register('client_message_handler')
class ItemlistHandler(object):
    message_type = 'N_ITEMLIST'

    @staticmethod
    def handle(client, room, message):
        room.on_client_item_list(client, message['items'])


@register('client_message_handler')
class BasesHandler(object):
    message_type = 'N_BASES'

    @staticmethod
    def handle(client, room, message):
        room.on_client_base_list(client, message['bases'])


@register('client_message_handler')
class InitflagsHandler(object):
    message_type = 'N_INITFLAGS'

    @staticmethod
    def handle(client, room, message):
        room.on_client_flag_list(client, message['flags'])


@register('client_message_handler')
class GunselectHandler(object):
    message_type = 'N_GUNSELECT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_gunselect(player, message['gunselect'])


@register('client_message_handler')
class ShootHandler(object):
    message_type = 'N_SHOOT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        shot_id = message['shot_id']
        gun = message['gun']
        from_pos = vec(*dictget(message, 'fx', 'fy', 'fz'))
        to_pos = vec(*dictget(message, 'tx', 'ty', 'tz'))
        hits = message['hits']
        room.on_player_shoot(player, shot_id, gun, from_pos, to_pos, hits)


@register('client_message_handler')
class ExplodeHandler(object):
    message_type = 'N_EXPLODE'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        cmillis = message['cmillis']
        gun = message['gun']
        explode_id = message['explode_id']
        hits = message['hits']
        room.on_player_explode(player, cmillis, gun, explode_id, hits)


@register('client_message_handler')
class ItempickupHandler(object):
    message_type = 'N_ITEMPICKUP'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_pickup_item(player, message['item_index'])


@register('client_message_handler')
class RepammoHandler(object):
    message_type = 'N_REPAMMO'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_replenish_ammo(player)


@register('client_message_handler')
class TakeflagHandler(object):
    message_type = 'N_TAKEFLAG'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_take_flag(player, message['flag'], message['version'])


@register('client_message_handler')
class TrydropflagHandler(object):
    message_type = 'N_TRYDROPFLAG'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_try_drop_flag(player)


@register('client_message_handler')
class PausegameHandler(object):
    message_type = 'N_PAUSEGAME'

    @staticmethod
    def handle(client, room, message):
        room.on_client_pause_game(client, message['value'])


@register('client_message_handler')
class TextHandler(object):
    message_type = 'N_TEXT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.on_player_game_chat(player, message['text'])


@register('client_message_handler')
class SayteamHandler(object):
    message_type = 'N_SAYTEAM'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.on_player_team_chat(player, message['text'])


@register('client_message_handler')
class SuicideHandler(object):
    message_type = 'N_SUICIDE'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_suicide(player)


@register('client_message_handler')
class TryspawnHandler(object):
    message_type = 'N_TRYSPAWN'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_request_spawn(player)


@register('client_message_handler')
class TauntHandler(object):
    message_type = 'N_TAUNT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.on_player_taunt(player)


@register('client_message_handler')
class ForceintermissionHandler(object):
    message_type = 'N_FORCEINTERMISSION'

    @staticmethod
    def handle(client, room, message):
        pass


@register('client_message_handler')
class TeleportHandler(object):
    message_type = 'N_TELEPORT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_teleport(player, message['teleport'], message['teledest'])


@register('client_message_handler')
class JumppadHandler(object):
    message_type = 'N_JUMPPAD'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.on_player_jumppad(player, message['jumppad'])


@register('client_message_handler')
class EditmodeHandler(object):
    message_type = 'N_EDITMODE'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        room.on_player_edit_mode(player, message['value'])


@register('client_message_handler')
class EditentHandler(object):
    message_type = 'N_EDITENT'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player()
        entity_id = message['entid']
        entity_type = message['type']
        x, y, z = dictget(message, 'x', 'y', 'z')
        attrs = message['attrs']
        room.on_player_edit_entity(player, entity_id, entity_type, x, y, z, attrs)


@register('client_message_handler')
class EditfHandler(object):
    message_type = 'N_EDITF'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        direction = message['direction']
        mode = message['mode']
        room.on_player_edit_face(player, selection, direction, mode)


@register('client_message_handler')
class EdittHandler(object):
    message_type = 'N_EDITT'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        texture = message['texture']
        all_faces = message['all_faces']
        room.on_player_edit_texture(player, selection, texture, all_faces)


@register('client_message_handler')
class EditmHandler(object):
    message_type = 'N_EDITM'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        material = message['material']
        material_filter = message['material_filter']
        room.on_player_edit_material(player, selection, material, material_filter)


@register('client_message_handler')
class FlipHandler(object):
    message_type = 'N_FLIP'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        room.on_player_edit_flip(player, selection)


@register('client_message_handler')
class CopyHandler(object):
    message_type = 'N_COPY'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        room.on_player_edit_copy(player, selection)


@register('client_message_handler')
class PasteHandler(object):
    message_type = 'N_PASTE'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        room.on_player_edit_paste(player, selection)


@register('client_message_handler')
class DelcubeHandler(object):
    message_type = 'N_DELCUBE'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        room.on_player_edit_delete_cubes(player, selection)


@register('client_message_handler')
class RotateHandler(object):
    message_type = 'N_ROTATE'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        axis = message['axis']
        room.on_player_edit_rotate(player, selection, axis)


@register('client_message_handler')
class ReplaceHandler(object):
    message_type = 'N_REPLACE'

    @staticmethod
    def handle(client, room, message):
        del message['aiclientnum']
        player = client.get_player()
        selection = Selection.from_message(message)
        texture = message['texture']
        new_texture = message['new_texture']
        in_selection = message['in_selection']
        room.on_player_edit_replace(player, selection, texture, new_texture, in_selection)


@register('client_message_handler')
class RemipHandler(object):
    message_type = 'N_REMIP'

    @staticmethod
    def handle(client, room, message):
        room.on_client_edit_remip(client)


@register('client_message_handler')
class NewmapHandler(object):
    message_type = 'N_NEWMAP'

    @staticmethod
    def handle(client, room, message):
        room.on_client_edit_new_map(client, message['size'])


@register('client_message_handler')
class GetmapHandler(object):
    message_type = 'N_GETMAP'

    @staticmethod
    def handle(client, room, message):
        room.on_client_edit_get_map(client)


@register('client_message_handler')
class ClipboardHandler(object):
    message_type = 'N_CLIPBOARD'

    @staticmethod
    def handle(client, room, message):
        pass


@register('client_message_handler')
class EditvarHandler(object):
    message_type = 'N_EDITVAR'

    @staticmethod
    def handle(client, room, message):
        pass


@register('client_message_handler')
class MastermodeHandler(object):
    message_type = 'N_MASTERMODE'

    @staticmethod
    def handle(client, room, message):
        room.on_client_set_master_mode(client, message['mastermode'])


@register('client_message_handler')
class KickHandler(object):
    message_type = 'N_KICK'

    @staticmethod
    def handle(client, room, message):
        room.on_client_kick(client, message['target_cn'], message['reason'])


@register('client_message_handler')
class ClearbansHandler(object):
    message_type = 'N_CLEARBANS'

    @staticmethod
    def handle(client, room, message):
        room.on_client_clear_bans(client)


@register('client_message_handler')
class SetmasterHandler(object):
    message_type = 'N_SETMASTER'

    @staticmethod
    def handle(client, room, message):
        room.on_client_set_master(client, message['target_cn'], message['pwdhash'], message['value'])


@register('client_message_handler')
class ListdemosHandler(object):
    message_type = 'N_LISTDEMOS'

    @staticmethod
    def handle(client, room, message):
        room.on_client_list_demos(client)


@register('client_message_handler')
class CleardemosHandler(object):
    message_type = 'N_CLEARDEMOS'

    @staticmethod
    def handle(client, room, message):
        room.on_client_clear_demo(client, message['demonum'])


@register('client_message_handler')
class GetdemoHandler(object):
    message_type = 'N_GETDEMO'

    @staticmethod
    def handle(client, room, message):
        room.on_client_get_demo(client, message['demonum'])


@register('client_message_handler')
class RecorddemoHandler(object):
    message_type = 'N_RECORDDEMO'

    @staticmethod
    def handle(client, room, message):
        room.on_client_set_demo_recording(client, message['value'])


@register('client_message_handler')
class StopdemoHandler(object):
    message_type = 'N_STOPDEMO'

    @staticmethod
    def handle(client, room, message):
        room.on_client_stop_demo_recording(client)


@register('client_message_handler')
class GamespeedHandler(object):
    message_type = 'N_GAMESPEED'

    @staticmethod
    def handle(client, room, message):
        room.on_client_set_game_speed(client, message['value'])


@register('client_message_handler')
class AddbotHandler(object):
    message_type = 'N_ADDBOT'

    @staticmethod
    def handle(client, room, message):
        room.on_client_add_bot(client, message['skill'])


@register('client_message_handler')
class DelbotHandler(object):
    message_type = 'N_DELBOT'

    @staticmethod
    def handle(client, room, message):
        room.on_client_delete_bot(client)


@register('client_message_handler')
class BotlimitHandler(object):
    message_type = 'N_BOTLIMIT'

    @staticmethod
    def handle(client, room, message):
        room.on_client_set_bot_limit(client, message['limit'])


@register('client_message_handler')
class BotbalanceHandler(object):
    message_type = 'N_BOTBALANCE'

    @staticmethod
    def handle(client, room, message):
        room.on_client_set_bot_balance(client, message['balance'])


@register('client_message_handler')
class CheckmapsHandler(object):
    message_type = 'N_CHECKMAPS'

    @staticmethod
    def handle(client, room, message):
        room.on_client_check_maps(client)


@register('client_message_handler')
class ServcmdHandler(object):
    message_type = 'N_SERVCMD'

    @staticmethod
    def handle(client, room, message):
        room.on_client_command(client, message['command'])

