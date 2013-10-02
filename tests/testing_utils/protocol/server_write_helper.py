def put_info_reply(data_stream, server_desc, numclients, maxclients, mode_num, map_name, seconds_left, mastermask, gamepaused, gamespeed):
    message_data = {
        'server_desc': server_desc,
        'numclients': numclients,
        'maxclients': maxclients,
        'mode_num': mode_num,
        'map_name': map_name,
        'seconds_left': seconds_left,
        'mastermask': mastermask,
        'gamepaused': gamepaused,
        'gamespeed': gamespeed,
    }
    message = ('info_reply', message_data)
    data_stream.append(message)

def put_servinfo(data_stream, client, haspwd, description, domain):
    message_data = {
        'client':           client,
        'haspwd':           haspwd,
        'description':      description,
        'domain':           domain,
    }
    message = ('N_SERVINFO', message_data)
    data_stream.append(message)

def put_welcome(data_stream):
    message = ('N_WELCOME', {})
    data_stream.append(message)
    
def put_mastermode(data_stream, mastermode):
    message_data = {
        'mastermode':        mastermode,
    }
    message = ('N_MASTERMODE', message_data)
    data_stream.append(message)
    
def put_currentmaster(data_stream, mastermode, clients):
    message_data = {
        'mastermode':        mastermode,
        'clients':           clients,
    }
    message = ('N_CURRENTMASTER', message_data)
    data_stream.append(message)
    
def put_servmsg(data_stream, message):
    message_data = {
        'message':        message,
    }
    message = ('N_SERVMSG', message_data)
    data_stream.append(message)
    
def put_mapchange(data_stream, map_name, mode_num, hasitems):
    message_data = {
        'map_name':        map_name,
        'mode_num':        mode_num,
        'hasitems':        hasitems,
    }
    message = ('N_MAPCHANGE', message_data)
    data_stream.append(message)
    
def put_mapreload(data_stream):
    message = ('N_MAPRELOAD', {})
    data_stream.append(message)
    
def put_timeup(data_stream, timeleft):
    message_data = {
        'timeleft':        timeleft,
    }
    message = ('N_TIMEUP', message_data)
    data_stream.append(message)
    
def put_pausegame(data_stream, paused, client=None):
    message_data = {
        'paused':        paused,
        'client':        client,
    }
    message = ('N_PAUSEGAME', message_data)
    data_stream.append(message)
    
def put_spectator(data_stream, client, spectated):
    message_data = {
        'client':        client,
        'spectated':     spectated,
    }
    message = ('N_SPECTATOR', message_data)
    data_stream.append(message)
    
def put_setteam(data_stream, client, reason):
    message_data = {
        'client':        client,
        'reason':        reason,
    }
    message = ('N_SETTEAM', message_data)
    data_stream.append(message)

def put_initai(data_stream, aiclient):
    message_data = {
        'aiclient':     aiclient,
    }
    message = ('N_INITAI', message_data)
    data_stream.append(message)

def put_initclient(data_stream, client):
    message_data = {
        'client':        client,
    }
    message = ('N_INITCLIENT', message_data)
    data_stream.append(message)

def put_initclients(data_stream, clients):
    for client in clients:
        if client.isai:
            put_initai(data_stream, client)
        else:
            put_initclient(data_stream, client)
    
def put_resume(data_stream, players):
    message_data = {
        'players':        players,
    }
    message = ('N_RESUME', message_data)
    data_stream.append(message)
    
def put_itemacc(data_stream, item, client):
    message_data = {
        'item':        item,
        'client':        client,
    }
    message = ('N_ITEMACC', message_data)
    data_stream.append(message)
    
def put_announce(data_stream, item):
    message_data = {
        'item':        item,
    }
    message = ('N_ANNOUNCE', message_data)
    data_stream.append(message)
    
def put_itemspawn(data_stream, item):
    message_data = {
        'item':        item,
    }
    message = ('N_ITEMSPAWN', message_data)
    data_stream.append(message)
    
def put_itemlist(data_stream, items):
    message_data = {
        'items':        items,
    }
    message = ('N_ITEMLIST', message_data)
    data_stream.append(message)
    
def put_initflags(data_stream, teamscores, flags):
    message_data = {
        'teamscores':        teamscores,
        'flags':        flags,
    }
    message = ('N_INITFLAGS', message_data)
    data_stream.append(message)
                
def put_dropflag(data_stream, client, flag):
    message_data = {
        'client':        client,
        'flag':        flag,
    }
    message = ('N_DROPFLAG', message_data)
    data_stream.append(message)
    
def put_scoreflag(data_stream, client, relayflag, goalflag):
    message_data = {
        'client':        client,
        'relayflag':     relayflag,
        'goalflag':      goalflag,
    }
    message = ('N_SCOREFLAG', message_data)
    data_stream.append(message)
    
def put_returnflag(data_stream, client, flag):
    message_data = {
        'client':        client,
        'flag':        flag,
    }
    message = ('N_RETURNFLAG', message_data)
    data_stream.append(message)
    
def put_takeflag(data_stream, client, flag):
    message_data = {
        'client':        client,
        'flag':        flag,
    }
    message = ('N_TAKEFLAG', message_data)
    data_stream.append(message)
    
def put_resetflag(data_stream, flag, team):
    message_data = {
        'flag':        flag,
        'team':        team,
    }
    message = ('N_RESETFLAG', message_data)
    data_stream.append(message)

def put_invisflag(data_stream, flag):
    message_data = {
        'flag':        flag,
    }
    message = ('N_INVISFLAG', message_data)
    data_stream.append(message)
    
def put_bases(data_stream, bases):
    message_data = {
        'bases':        bases,
    }
    message = ('N_BASES', message_data)
    data_stream.append(message)
        
def put_baseinfo(data_stream, base):
    message_data = {
        'base':        base,
    }
    message = ('N_BASEINFO', message_data)
    data_stream.append(message)
    
def put_basescore(data_stream, base):
    message_data = {
        'base':        base,
    }
    message = ('N_BASESCORE', message_data)
    data_stream.append(message)
    
def put_repammo(data_stream, client, base):
    message_data = {
        'client':        client,
        'base':        base,
    }
    message = ('N_REPAMMO', message_data)
    data_stream.append(message)
    
def put_baseregen(data_stream, client, base):
    message_data = {
        'client':        client,
        'base':        base,
    }
    message = ('N_BASEREGEN', message_data)
    data_stream.append(message)
    
def put_cdis(data_stream, client):
    message_data = {
        'client':        client,
    }
    message = ('N_CDIS', message_data)
    data_stream.append(message)
    
def put_died(data_stream, client, killer):
    message_data = {
        'client':        client,
        'killer':        killer,
    }
    message = ('N_DIED', message_data)
    data_stream.append(message)
    
def put_forcedeath(data_stream, client):
    message_data = {
        'client':        client,
    }
    message = ('N_FORCEDEATH', message_data)
    data_stream.append(message)
    
def put_jumppad(data_stream, client, jumppad):
    message_data = {
        'client':        client,
        'jumppad':        jumppad,
    }
    message = ('N_JUMPPAD', message_data)
    data_stream.append(message)
    
def put_teleport(data_stream, client, teleport, teledest):
    message_data = {
        'client':        client,
        'teleport':        teleport,
        'teledest':        teledest,
    }
    message = ('N_TELEPORT', message_data)
    data_stream.append(message)
    
def put_shotfx(data_stream, client, gun, shot_id, fx, fy, fz, tx, ty, tz):
    message_data = {
        'client':    client,
        'gun':       gun,
        'shot_id':   shot_id,
        
        'fx':        fx,
        'fy':        fy,
        'fz':        fz,
        
        'tx':        tx,
        'ty':        ty,
        'tz':        tz,
    }
    message = ('N_SHOTFX', message_data)
    data_stream.append(message)
    
def put_explodefx(data_stream, client, gun, explode_id):
    message_data = {
        'client':     client,
        'gun':        gun,
        'explode_id': explode_id,
    }
    message = ('N_EXPLODEFX', message_data)
    data_stream.append(message)
    
def put_damage(data_stream, target, client, damage):
    message_data = {
        'target':        target,
        'client':        client,
        'damage':        damage,
    }
    message = ('N_DAMAGE', message_data)
    data_stream.append(message)
    
def put_hitpush(data_stream, target, gun, damage, v):
    message_data = {
        'target':   target,
        'gun':      gun,
        'damage':   damage,
        'v':        v,
    }
    message = ('N_HITPUSH', message_data)
    data_stream.append(message)
    
def put_spawnstate(data_stream, player):
    message_data = {
        'player':        player,
    }
    message = ('N_SPAWNSTATE', message_data)
    data_stream.append(message)
    
def put_spawn(data_stream, player_state):
    message_data = {
        'player_state':        player_state,
    }
    message = ('N_SPAWN', message_data)
    data_stream.append(message)
    
def put_pong(data_stream, cmillis):
    message_data = {
        'cmillis':        cmillis,
    }
    message = ('N_PONG', message_data)
    data_stream.append(message)
    
def put_clientping(data_stream, ping):
    message_data = {
        'ping':        ping,
    }
    message = ('N_CLIENTPING', message_data)
    data_stream.append(message)
    
def put_switchname(data_stream, name):
    message_data = {
        'name':        name,
    }
    message = ('N_SWITCHNAME', message_data)
    data_stream.append(message)
    
def put_gunselect(data_stream, gunselect):
    message_data = {
        'gunselect':        gunselect,
    }
    message = ('N_GUNSELECT', message_data)
    data_stream.append(message)
    
def put_sound(data_stream, sound):
    message_data = {
        'sound':        sound,
    }
    message = ('N_SOUND', message_data)
    data_stream.append(message)
    
def put_clientdata(data_stream, client, data):
    message_data = {
        'client':      client,
        'data':        data,
    }
    message = ('N_CLIENT', message_data)
    data_stream.append(message)
    
def put_text(data_stream, text):
    message_data = {
        'text':        text,
    }
    message = ('N_TEXT', message_data)
    data_stream.append(message)
    
def put_sayteam(data_stream, client, text):
    message_data = {
        'client':      client,
        'text':        text,
    }
    message = ('N_SAYTEAM', message_data)
    data_stream.append(message)
   
def put_authchall(data_stream, desc, auth_id, challenge):
    message_data = {
        'desc':        desc,
        'auth_id':     auth_id,
        'challenge':   challenge,
    }
    message = ('N_AUTHCHAL', message_data)
    data_stream.append(message)
    
def put_newmap(data_stream, size):
    message_data = {
        'size':        size,
    }
    message = ('N_NEWMAP', message_data)
    data_stream.append(message)
    
def put_editent(data_stream, ent_id, v, ent_type, attrs):
    message_data = {
        'ent_id':       ent_id,
        'v':            v,
        'ent_type':     ent_type,
        'attrs':        attrs,
    }
    message = ('N_EDITENT', message_data)
    data_stream.append(message)
        
def put_editf(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner, move_dir, mode_mode):
    message_data = {
                    'sel_o': sel_o,
                    'sel_s': sel_s,
                    'sel_grid': sel_grid,
                    'sel_orient': sel_orient,
                    'sel_cx': sel_cx,
                    'sel_cxs': sel_cxs,
                    'sel_cy': sel_cy,
                    'sel_cys': sel_cys,
                    'sel_corner': sel_corner,
                    'move_dir': move_dir,
                    'mode_mode': mode_mode,
    }
    message = ('N_EDITF', message_data)
    data_stream.append(message)
    
def put_editt(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner, tex, allfaces):
    message_data = {
                    'sel_o': sel_o,
                    'sel_s': sel_s,
                    'sel_grid': sel_grid,
                    'sel_orient': sel_orient,
                    'sel_cx': sel_cx,
                    'sel_cxs': sel_cxs,
                    'sel_cy': sel_cy,
                    'sel_cys': sel_cys,
                    'sel_corner': sel_corner,
                    'tex': tex,
                    'allfaces': allfaces,
    }
    message = ('N_EDITT', message_data)
    data_stream.append(message)

def put_delcube(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner):
    message_data = {
                    'sel_o': sel_o,
                    'sel_s': sel_s,
                    'sel_grid': sel_grid,
                    'sel_orient': sel_orient,
                    'sel_cx': sel_cx,
                    'sel_cxs': sel_cxs,
                    'sel_cy': sel_cy,
                    'sel_cys': sel_cys,
                    'sel_corner': sel_corner,
    }
    message = ('N_DELCUBE', message_data)
    data_stream.append(message)
