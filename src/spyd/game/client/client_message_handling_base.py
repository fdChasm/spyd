import traceback

from cube2common.constants import disconnect_types, MAXNAMELEN, MAXTEAMLEN
from cube2common.vec import vec
from spyd.game.edit.selection import Selection
from spyd.game.server_message_formatter import info, denied, error, smf
from spyd.protocol import swh
from spyd.utils.dictionary_get import dictget
from spyd.utils.filtertext import filtertext


class GenericError(Exception):
    def __init__(self, message_fmt, *fmt_args, **fmt_kwargs):
        self.message = smf.vformat(message_fmt, fmt_args, fmt_kwargs)
        
class InsufficientPermissions(GenericError): pass
class UnknownPlayer(GenericError):
    def __init__(self, cn=None, name=None):
        if cn is not None:
            message_fmt = 'No player with cn {cn#cn} found.'
            fmt_kwargs = {'cn': cn}
        elif name is not None:
            message_fmt = 'Could not resolve name {name#name} to a player.'
            fmt_kwargs = {'name': name}
        else:
            message_fmt = 'Unknown player.'
            fmt_kwargs = {}
        GenericError.__init__(self, message_fmt, **fmt_kwargs)

class ClientMessageHandlingBase(object):
    def _message_received(self, message_type, message):
        try:
            if (not self.is_connected) and message_type != "N_CONNECT":
                self.disconnect(disconnect_types.DISC_TAGT)
                return
            else:
                if hasattr(self, message_type):
                    handler = getattr(self, message_type)
                    try:
                        handler(message)
                    except InsufficientPermissions as e:
                        self.send_server_message(denied(e.message))
                    except GenericError as e:
                        self.send_server_message(error(e.message))
                else:
                    print "Client received unhandled message type:", message_type, message
        except:
            traceback.print_exc()
        
    def N_CONNECT(self, message):
            if not self.is_connected:
                self.connect_received(message)
                
    def N_PING(self, message):
        with self.sendbuffer(1, False) as cds:
            swh.put_pong(cds, message['cmillis'])

    def N_CLIENTPING(self, message):
        ping = message['ping']
        self.ping_buffer.add(ping)
        player = self.get_player()
        swh.put_clientping(player.state.messages, ping)

    def N_POS(self, message):
        player = self.get_player(message['clientnum'])
        player.state.update_position(message['position'], message['raw_position'])

    def N_SOUND(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_sound(player, message['sound'])

    def N_SPAWN(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_spawn(player, message['lifesequence'], message['gunselect'])
        
    def N_SWITCHMODEL(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_switch_model(player, message['playermodel'])
        
    def N_SWITCHNAME(self, message):
        player = self.get_player(-1)
        name = filtertext(message['name'], False, MAXNAMELEN)
        if len(name) <= 0:
            name = "unnamed"
        self.room.on_player_switch_name(player, name)
        
    def N_SWITCHTEAM(self, message):
        player = self.get_player(-1)
        team_name = filtertext(message['team'], False, MAXTEAMLEN)
        self.room.on_player_switch_team(player, team_name)
        
    def N_SETTEAM(self, message):
        team_name = filtertext(message['team'], False, MAXTEAMLEN)
        self.room.on_client_set_team(self, message['target_cn'], team_name)
        
    def N_SPECTATOR(self, message):
        self.room.on_client_set_spectator(self, message['target_cn'], bool(message['value']))
                                          
    def N_MAPVOTE(self, message):
        self.room.on_client_map_vote(self, message['map_name'], message['mode_num'])
                                          
    def N_MAPCHANGE(self, message):
        self.room.on_client_map_vote(self, message['map_name'], message['mode_num'])
        
    def N_MAPCRC(self, message):
        self.room.on_client_map_crc(self, message['mapcrc'])

    def N_AUTHANS(self, message):
        authdomain = message['authdomain']
        authid = message['authid']
        answer = message['answer']
        self.answer_auth_challenge(authdomain, authid, answer)

    def N_AUTHTRY(self, message):
        authdomain = message['authdomain']
        authname = message['authname']
        deferred = self.auth(authdomain, authname)
        
    def N_AUTHKICK(self, message):
        authdomain = message['authdomain']
        authname = message['authname']
        target_pn = message['target_cn']
        reason = message['reason']
        deferred = self.auth(authdomain, authname)
        deferred.addCallback(lambda a: self.room.on_client_kick(self, target_pn, reason))
        
    def N_ITEMLIST(self, message):
        self.room.on_client_item_list(self, message['items'])

    def N_BASES(self, message):
        self.room.on_client_base_list(self, message['bases'])

    def N_INITFLAGS(self, message):
        self.room.on_client_flag_list(self, message['flags'])
        
    def N_GUNSELECT(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_gunselect(player, message['gunselect'])
        
    def N_SHOOT(self, message):
        player = self.get_player(message['aiclientnum'])
        shot_id = message['shot_id']
        gun = message['gun']
        from_pos = vec(*dictget(message, 'fx', 'fy', 'fz'))
        to_pos = vec(*dictget(message, 'tx', 'ty', 'tz'))
        hits = message['hits']
        self.room.on_player_shoot(player, shot_id, gun, from_pos, to_pos, hits)
        
    def N_EXPLODE(self, message):
        player = self.get_player(message['aiclientnum'])
        cmillis = message['cmillis']
        gun = message['gun']
        explode_id = message['explode_id']
        hits = message['hits']
        self.room.on_player_explode(player, cmillis, gun, explode_id, hits)
        
    def N_ITEMPICKUP(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_pickup_item(player, message['item_index'])
        
    def N_REPAMMO(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_replenish_ammo(player)
        
    def N_TAKEFLAG(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_take_flag(player, message['flag'], message['version'])
        
    def N_TRYDROPFLAG(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_try_drop_flag(player)
        
    def N_PAUSEGAME(self, message):
        self.room.on_client_pause_game(self, message['value'])
        
    def N_TEXT(self, message):
        player = self.get_player()
        self.room.on_player_game_chat(player, message['text'])
        
    def N_SAYTEAM(self, message):
        player = self.get_player()
        self.room.on_player_team_chat(player, message['text'])
        
    def N_SUICIDE(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_suicide(player)
        
    def N_TRYSPAWN(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_request_spawn(player)
        
    def N_TAUNT(self, message):
        player = self.get_player()
        self.room.on_player_taunt(player)
        
    def N_FORCEINTERMISSION(self, message):
        pass

    def N_TELEPORT(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_teleport(player, message['teleport'], message['teledest'])
        
    def N_JUMPPAD(self, message):
        player = self.get_player(message['aiclientnum'])
        self.room.on_player_jumppad(player, message['jumppad'])
        
    def N_EDITMODE(self, message):
        player = self.get_player()
        self.room.on_player_edit_mode(player, message['value'])
        
    def N_EDITENT(self, message):
        player = self.get_player()
        entity_id = message['entid']
        entity_type = message['type']
        x, y, z = dictget(message, 'x', 'y', 'z')
        attrs = message['attrs']
        self.room.on_player_edit_entity(player, entity_id, entity_type, x, y, z, attrs)
        
    def N_EDITF(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        direction = message['direction']
        mode = message['mode']
        self.room.on_player_edit_face(player, selection, direction, mode)
        
    def N_EDITT(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        texture = message['texture']
        all_faces = message['all_faces']
        self.room.on_player_edit_texture(player, selection, texture, all_faces)
        
    def N_EDITM(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        material = message['material']
        material_filter = message['material_filter']
        self.room.on_player_edit_material(player, selection, material, material_filter)
        
    def N_FLIP(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        self.room.on_player_edit_flip(player, selection)
        
    def N_COPY(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        self.room.on_player_edit_copy(player, selection)
        
    def N_PASTE(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        self.room.on_player_edit_paste(player, selection)
        
    def N_DELCUBE(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        self.room.on_player_edit_delete_cubes(player, selection)
        
    def N_ROTATE(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        axis = message['axis']
        self.room.on_player_edit_rotate(player, selection, axis)
        
    def N_REPLACE(self, message):
        del message['aiclientnum']
        player = self.get_player()
        selection = Selection.from_message(message)
        texture = message['texture']
        new_texture = message['new_texture']
        in_selection = message['in_selection']
        self.room.on_player_edit_replace(player, selection, texture, new_texture, in_selection)
        
    def N_REMIP(self, message):
        self.room.on_client_edit_remip(self)
        
    def N_NEWMAP(self, message):
        self.room.on_client_edit_new_map(self, message['size'])
        
    def N_GETMAP(self, message):
        self.room.on_client_edit_get_map(self)
        
    def N_CLIPBOARD(self, message):
        pass
    
    def N_EDITVAR(self, message):
        pass
    
    def N_MASTERMODE(self, message):
        self.room.on_client_set_master_mode(self, message['mastermode'])
        
    def N_KICK(self, message):
        self.room.on_client_kick(self, message['target_cn'], message['reason'])
        
    def N_CLEARBANS(self, message):
        self.room.on_client_clear_bans(self)
        
    def N_SETMASTER(self, message):
        self.room.on_client_set_master(self, message['target_cn'], message['pwdhash'], message['value'])
        
    def N_LISTDEMOS(self, message):
        self.room.on_client_list_demos(self)
        
    def N_CLEARDEMOS(self, message):
        self.room.on_client_clear_demo(self, message['demonum'])
        
    def N_GETDEMO(self, message):
        self.room.on_client_get_demo(self, message['demonum'])
        
    def N_RECORDDEMO(self, message):
        self.room.on_client_set_demo_recording(self, message['value'])
        
    def N_STOPDEMO(self, message):
        self.room.on_client_stop_demo_recording(self)
        
    def N_GAMESPEED(self, message):
        self.room.on_client_set_game_speed(self, message['value'])
        
    def N_ADDBOT(self, message):
        self.room.on_client_add_bot(self, message['skill'])
        
    def N_DELBOT(self, message):
        self.room.on_client_delete_bot(self)
        
    def N_BOTLIMIT(self, message):
        self.room.on_client_set_bot_limit(self, message['limit'])
        
    def N_BOTBALANCE(self, message):
        self.room.on_client_set_bot_balance(self, message['balance'])
        
    def N_CHECKMAPS(self, message):
        self.room.on_client_check_maps(self)
    
    def N_SERVCMD(self, message):
        self.room.on_client_command(self, message['command'])
