from cube2common.constants import PROTOCOL_VERSION, message_types, weapon_types, privileges
from spyd.utils.formatted_sauerbraten_message_splitter import FormattedSauerbratenMessageSplitter


def put_info_reply(cds, server_desc, numclients, maxclients, mode_num, map_name, seconds_left, mastermask, gamepaused, gamespeed):
    cds.putint(numclients)
    cds.putint(7)  # fields following
    cds.putint(PROTOCOL_VERSION)
    cds.putint(mode_num)
    cds.putint(seconds_left)
    cds.putint(maxclients)
    cds.putint(mastermask)
    cds.putint(1 if gamepaused else 0)
    cds.putint(gamespeed)
    cds.putstring(map_name)
    cds.putstring(server_desc)

def put_servinfo(data_stream, client, haspwd, description, domain):
    data_stream.putint(message_types.N_SERVINFO)
    data_stream.putint(client.cn)
    data_stream.putint(PROTOCOL_VERSION)
    data_stream.putint(id(client))
    data_stream.putint(haspwd)
    data_stream.putstring(description)
    data_stream.putstring(domain)

def put_welcome(data_stream):
    data_stream.putint(message_types.N_WELCOME)

def put_mastermode(data_stream, mastermode):
    data_stream.putint(message_types.N_MASTERMODE)
    data_stream.putint(mastermode)

def put_currentmaster(data_stream, mastermode, clients):
    data_stream.putint(message_types.N_CURRENTMASTER)
    data_stream.putint(mastermode)
    for client in clients:
        if client.privilege > privileges.PRIV_NONE:
            data_stream.putint(client.cn)
            data_stream.putint(client.privilege)
    data_stream.putint(-1)

def put_raw_servmsg(data_stream, message):
    data_stream.putint(message_types.N_SERVMSG)
    data_stream.putstring(message)

def put_servmsg(data_stream, message):
    message_splitter = FormattedSauerbratenMessageSplitter(max_length=512)
    messages = message_splitter.split(message)
    for message in messages:
        put_raw_servmsg(data_stream, message)

def put_mapchange(data_stream, map_name, mode_num, hasitems):
    data_stream.putint(message_types.N_MAPCHANGE)
    data_stream.putstring(map_name)
    data_stream.putint(mode_num)
    need_items = not hasitems
    data_stream.putint(1 if need_items else 0)

def put_mapreload(data_stream):
    data_stream.putint(message_types.N_MAPRELOAD)

def put_timeup(data_stream, timeleft):
    data_stream.putint(message_types.N_TIMEUP)
    data_stream.putint(timeleft)

def put_pausegame(data_stream, paused, client=None):
    data_stream.putint(message_types.N_PAUSEGAME)
    data_stream.putint(paused)
    data_stream.putint(client.cn if client is not None else -1)

def put_spectator(data_stream, player):
    data_stream.putint(message_types.N_SPECTATOR)
    data_stream.putint(player.pn)
    data_stream.putint(1 if player.state.is_spectator else 0)

def put_setteam(data_stream, client, reason):
    data_stream.putint(message_types.N_SETTEAM)
    data_stream.putint(client.cn)
    data_stream.putstring(client.team.name)
    data_stream.putint(reason)

def put_initai(data_stream, aiclient):
    data_stream.putint(message_types.N_INITAI)
    data_stream.putint(aiclient.cn)
    data_stream.putint(aiclient.owner.cn)
    data_stream.putint(aiclient.aitype)
    data_stream.putint(aiclient.aiskill)
    data_stream.putint(aiclient.playermodel)
    data_stream.putstring(aiclient.name)
    data_stream.putstring(aiclient.team)

def put_initclient(data_stream, client):
    data_stream.putint(message_types.N_INITCLIENT)
    data_stream.putint(client.cn)
    data_stream.putstring(client.name)
    data_stream.putstring(client.team.name if client.team is not None else "")
    data_stream.putint(client.playermodel)

def put_initclients(data_stream, clients):
    for client in clients:
        if client.isai:
            put_initai(data_stream, client)
        else:
            put_initclient(data_stream, client)

def put_state(data_stream, player_state):
    data_stream.putint(player_state.lifesequence)
    data_stream.putint(player_state.health)
    data_stream.putint(player_state.maxhealth)
    data_stream.putint(player_state.armour)
    data_stream.putint(player_state.armourtype)
    data_stream.putint(player_state.gunselect)

def put_ammo(data_stream, player_state):
    for ammo_slot in player_state.ammo[weapon_types.GUN_SG:weapon_types.GUN_PISTOL + 1]:
        data_stream.putint(ammo_slot)

def put_resume(data_stream, players):
    data_stream.putint(message_types.N_RESUME)
    for player in players:
        data_stream.putint(player.pn)
        data_stream.putint(player.state.state)
        data_stream.putint(player.state.frags)
        data_stream.putint(player.state.flags)
        data_stream.putint(player.state.quadremaining)

        put_state(data_stream, player.state)
        put_ammo(data_stream, player.state)

    data_stream.putint(-1)

def put_itemacc(data_stream, item, client):
    data_stream.putint(message_types.N_ITEMACC)
    data_stream.putint(item.index)
    data_stream.putint(client.cn)

def put_announce(data_stream, item):
    data_stream.putint(message_types.N_ANNOUNCE)
    data_stream.putint(item.type)

def put_itemspawn(data_stream, item):
    data_stream.putint(message_types.N_ITEMSPAWN)
    data_stream.putint(item.index)

def put_itemlist(data_stream, items):
    data_stream.putint(message_types.N_ITEMLIST)
    for item in items:
        if item.spawned:
            data_stream.putint(item.index)
            data_stream.putint(item.type)
    data_stream.putint(-1)

def put_teaminfo(data_stream, teams):
    data_stream.putint(message_types.N_TEAMINFO)
    for team in teams:
        data_stream.putstring(team.name)
        data_stream.putint(team.frags)
    data_stream.putstring('')

def put_initflags(data_stream, teamscores, flags):
    data_stream.putint(message_types.N_INITFLAGS)
    for score in teamscores:
        data_stream.putint(score)

    data_stream.putint(len(flags))
    for flag in flags:
        data_stream.putint(flag.version)
        data_stream.putint(flag.spawn)
        data_stream.putint(flag.owner.cn if flag.owner is not None else -1)
        data_stream.putint(flag.invisible)
        if flag.owner is None:
            data_stream.putint(flag.dropped)
            if flag.dropped:
                data_stream.putint(flag.drop_location.x)
                data_stream.putint(flag.drop_location.y)
                data_stream.putint(flag.drop_location.z)

def put_dropflag(data_stream, client, flag):
    data_stream.putint(message_types.N_DROPFLAG)
    data_stream.putint(client.cn)
    data_stream.putint(flag.id)
    data_stream.putint(flag.version)
    data_stream.putint(flag.drop_location.x)
    data_stream.putint(flag.drop_location.y)
    data_stream.putint(flag.drop_location.z)

def put_scoreflag(data_stream, client, relayflag, goalflag):
    data_stream.putint(message_types.N_SCOREFLAG)
    data_stream.putint(client.cn)
    data_stream.putint(relayflag.id)
    data_stream.putint(relayflag.version)
    data_stream.putint(goalflag.id)
    data_stream.putint(goalflag.version)
    data_stream.putint(goalflag.spawn)
    data_stream.putint(client.team.id + 1)
    data_stream.putint(client.team.score)
    data_stream.putint(client.state.flags)

def put_returnflag(data_stream, client, flag):
    data_stream.putint(message_types.N_RETURNFLAG)
    data_stream.putint(client.cn)
    data_stream.putint(flag.id)
    data_stream.putint(flag.version)

def put_takeflag(data_stream, client, flag):
    data_stream.putint(message_types.N_TAKEFLAG)
    data_stream.putint(client.cn)
    data_stream.putint(flag.id)
    data_stream.putint(flag.version)

def put_resetflag(data_stream, flag, team):
    data_stream.putint(message_types.N_RESETFLAG)
    data_stream.putint(flag.id)
    data_stream.putint(flag.version)
    data_stream.putint(flag.spawn)
    data_stream.putint(team.id)
    data_stream.putint(team.score)

def put_invisflag(data_stream, flag):
    data_stream.putint(message_types.N_INVISFLAG)
    data_stream.putint(flag.id)
    data_stream.putint(flag.invisible)

def put_bases(data_stream, bases):
    data_stream.putint(message_types.N_BASES)
    data_stream.putint(len(bases))
    for base in bases:
        data_stream.putint(base.ammotype)
        data_stream.putstring(base.ownerteam.name if base.ownerteam is not None else "")
        data_stream.putstring(base.enemyteam.name if base.enemyteam is not None else "")
        data_stream.putint(base.converted)
        data_stream.putint(base.ammocount)

def put_baseinfo(data_stream, base):
    data_stream.putint(message_types.N_BASEINFO)
    data_stream.putint(base.id)
    data_stream.putstring(base.ownerteam.name if base.ownerteam is not None else "")
    data_stream.putstring(base.enemyteam.name if base.enemyteam is not None else "")
    data_stream.putint(base.converted)
    data_stream.putint(base.ammocount)

def put_basescore(data_stream, base):
    data_stream.putint(message_types.N_BASESCORE)
    data_stream.putint(base.id)
    data_stream.putstring(base.ownerteam.name)
    data_stream.putint(base.ownerteam.score)

def put_repammo(data_stream, client, base):
    data_stream.putint(message_types.N_REPAMMO)
    data_stream.putint(client.cn)
    data_stream.putint(base.ammotype)

def put_baseregen(data_stream, client, base):
    data_stream.putint(message_types.N_BASEREGEN)
    data_stream.putint(client.cn)
    data_stream.putint(client.state.health)
    data_stream.putint(client.state.armour)
    data_stream.putint(base.ammotype)
    data_stream.putint(client.state.ammo[base.ammotype])

def put_cdis(data_stream, client):
    data_stream.putint(message_types.N_CDIS)
    data_stream.putint(client.cn)

def put_died(data_stream, client, killer):
    data_stream.putint(message_types.N_DIED)
    data_stream.putint(client.cn)
    data_stream.putint(killer.cn)
    data_stream.putint(killer.state.frags)
    if killer.team is not None:
        data_stream.putint(killer.team.frags)
    else:
        data_stream.putint(0)

def put_forcedeath(data_stream, client):
    data_stream.putint(message_types.N_FORCEDEATH)
    data_stream.putint(client.cn)

def put_jumppad(data_stream, client, jumppad):
    data_stream.putint(message_types.N_JUMPPAD)
    data_stream.putint(client.cn)
    data_stream.putint(jumppad)

def put_teleport(data_stream, client, teleport, teledest):
    data_stream.putint(message_types.N_TELEPORT)
    data_stream.putint(client.cn)
    data_stream.putint(teleport)
    data_stream.putint(teledest)

def put_shotfx(data_stream, client, gun, shot_id, from_pos, to_pos):
    data_stream.putint(message_types.N_SHOTFX)
    data_stream.putint(client.cn)
    data_stream.putint(gun)
    data_stream.putint(shot_id)
    data_stream.putint(from_pos.x)
    data_stream.putint(from_pos.y)
    data_stream.putint(from_pos.z)
    data_stream.putint(to_pos.x)
    data_stream.putint(to_pos.y)
    data_stream.putint(to_pos.z)

def put_explodefx(data_stream, client, gun, explode_id):
    data_stream.putint(message_types.N_EXPLODEFX)
    data_stream.putint(client.cn)
    data_stream.putint(gun)
    data_stream.putint(explode_id)

def put_damage(data_stream, target, client, damage):
    data_stream.putint(message_types.N_DAMAGE)
    data_stream.putint(target.cn)
    data_stream.putint(client.cn)
    data_stream.putint(damage)
    data_stream.putint(target.state.armour)
    data_stream.putint(target.state.health)

def put_hitpush(data_stream, target, gun, damage, v):
    data_stream.putint(message_types.N_HITPUSH)
    data_stream.putint(target.cn)
    data_stream.putint(gun)
    data_stream.putint(damage)
    data_stream.putint(v.x)
    data_stream.putint(v.y)
    data_stream.putint(v.z)

def put_spawnstate(data_stream, player):
    data_stream.putint(message_types.N_SPAWNSTATE)
    data_stream.putint(player.pn)
    put_state(data_stream, player.state)
    put_ammo(data_stream, player.state)

def put_spawn(data_stream, player_state):
    data_stream.putint(message_types.N_SPAWN)
    put_state(data_stream, player_state)
    put_ammo(data_stream, player_state)

def put_pong(data_stream, cmillis):
    data_stream.putint(message_types.N_PONG)
    data_stream.putint(cmillis)

def put_clientping(data_stream, ping):
    data_stream.putint(message_types.N_CLIENTPING)
    data_stream.putint(ping)

def put_switchname(data_stream, name):
    data_stream.putint(message_types.N_SWITCHNAME)
    data_stream.putstring(name)

def put_switchmodel(data_stream, playermodel):
    data_stream.putint(message_types.N_SWITCHMODEL)
    data_stream.putint(playermodel)

def put_taunt(data_stream):
    data_stream.putint(message_types.N_TAUNT)

def put_gunselect(data_stream, gunselect):
    data_stream.putint(message_types.N_GUNSELECT)
    data_stream.putint(gunselect)

def put_sound(data_stream, sound):
    data_stream.putint(message_types.N_SOUND)
    data_stream.putint(sound)

def put_clientdata(data_stream, client, data):
    data_stream.putint(message_types.N_CLIENT)
    data_stream.putint(client.cn)
    data_stream.putuint(len(data))
    data_stream.write(data)

def put_text(data_stream, text):
    data_stream.putint(message_types.N_TEXT)
    data_stream.putstring(text)

def put_sayteam(data_stream, client, text):
    data_stream.putint(message_types.N_SAYTEAM)
    data_stream.putint(client.cn)
    data_stream.putstring(text)

def put_authchall(data_stream, desc, auth_id, challenge):
    data_stream.putint(message_types.N_AUTHCHAL)
    data_stream.putstring(desc)
    data_stream.putint(auth_id)
    data_stream.putstring(challenge)

def put_newmap(data_stream, size):
    data_stream.putint(message_types.N_NEWMAP)
    data_stream.putint(size)

def put_vector(data_stream, v):
    data_stream.putint(v.x)
    data_stream.putint(v.y)
    data_stream.putint(v.z)
    
def put_editmode(data_stream, editmode):
    data_stream.putint(message_types.N_EDITMODE)
    data_stream.putint(1 if editmode else 0)

def put_editent(data_stream, ent_id, v, ent_type, attrs):
    assert(len(attrs) == 5)
    data_stream.putint(message_types.N_EDITENT)
    data_stream.putint(ent_id)
    put_vector(data_stream, v)
    data_stream.putint(ent_type)
    for attr in attrs:
        data_stream.putint(attr)

'''
common_edit_fields = [Field(name="sel_ox", type="int"),
                      Field(name="sel_oy", type="int"),
                      Field(name="sel_oz", type="int"),

                      Field(name="sel_sx", type="int"),
                      Field(name="sel_sy", type="int"),
                      Field(name="sel_sz", type="int"),

                      Field(name="sel_grid", type="int"),
                      Field(name="sel_orient", type="int"),

                      Field(name="sel_cx", type="int"),
                      Field(name="sel_cxs", type="int"),
                      Field(name="sel_cy", type="int"),
                      Field(name="sel_cys", type="int"),

                      Field(name="sel_corner", type="int")]
'''

def put_editf(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner, move_dir, mode_mode):
    data_stream.putint(message_types.N_EDITF)

    put_vector(data_stream, sel_o)
    put_vector(data_stream, sel_s)

    data_stream.putint(sel_grid)
    data_stream.putint(sel_orient)

    data_stream.putint(sel_cx)
    data_stream.putint(sel_cxs)
    data_stream.putint(sel_cy)
    data_stream.putint(sel_cys)

    data_stream.putint(sel_corner)

    data_stream.putint(move_dir)
    data_stream.putint(mode_mode)

def put_editt(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner, tex, allfaces):
    data_stream.putint(message_types.N_EDITT)

    put_vector(data_stream, sel_o)
    put_vector(data_stream, sel_s)

    data_stream.putint(sel_grid)
    data_stream.putint(sel_orient)

    data_stream.putint(sel_cx)
    data_stream.putint(sel_cxs)
    data_stream.putint(sel_cy)
    data_stream.putint(sel_cys)

    data_stream.putint(sel_corner)

    data_stream.putint(tex)
    data_stream.putint(allfaces)

def put_delcube(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner):
    data_stream.putint(message_types.N_DELCUBE)

    put_vector(data_stream, sel_o)
    put_vector(data_stream, sel_s)

    data_stream.putint(sel_grid)
    data_stream.putint(sel_orient)

    data_stream.putint(sel_cx)
    data_stream.putint(sel_cxs)
    data_stream.putint(sel_cy)
    data_stream.putint(sel_cys)

    data_stream.putint(sel_corner)
