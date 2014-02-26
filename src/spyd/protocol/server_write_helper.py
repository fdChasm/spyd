from cube2common.constants import PROTOCOL_VERSION, message_types, weapon_types, privileges
from spyd.utils.formatted_sauerbraten_message_splitter import FormattedSauerbratenMessageSplitter

class swh(object):
    @staticmethod
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

    @staticmethod
    def put_servinfo(data_stream, client, haspwd, description, domain):
        data_stream.putint(message_types.N_SERVINFO)
        data_stream.putint(client.cn)
        data_stream.putint(PROTOCOL_VERSION)
        data_stream.putint(id(client))
        data_stream.putint(haspwd)
        data_stream.putstring(description)
        data_stream.putstring(domain)

    @staticmethod
    def put_welcome(data_stream):
        data_stream.putint(message_types.N_WELCOME)

    @staticmethod
    def put_mastermode(data_stream, mastermode):
        data_stream.putint(message_types.N_MASTERMODE)
        data_stream.putint(mastermode)

    @staticmethod
    def put_currentmaster(data_stream, mastermode, clients):
        data_stream.putint(message_types.N_CURRENTMASTER)
        data_stream.putint(mastermode)
        for client in clients:
            if client.privilege > privileges.PRIV_NONE:
                data_stream.putint(client.cn)
                data_stream.putint(client.privilege)
        data_stream.putint(-1)

    @staticmethod
    def put_raw_servmsg(data_stream, message):
        data_stream.putint(message_types.N_SERVMSG)
        data_stream.putstring(message)

    @staticmethod
    def put_servmsg(data_stream, message):
        message_splitter = FormattedSauerbratenMessageSplitter(max_length=512)
        messages = message_splitter.split(message)
        for message in messages:
            swh.put_raw_servmsg(data_stream, message)

    @staticmethod
    def put_mapchange(data_stream, map_name, mode_num, hasitems):
        data_stream.putint(message_types.N_MAPCHANGE)
        data_stream.putstring(map_name)
        data_stream.putint(mode_num)
        need_items = not hasitems
        data_stream.putint(1 if need_items else 0)

    @staticmethod
    def put_mapreload(data_stream):
        data_stream.putint(message_types.N_MAPRELOAD)

    @staticmethod
    def put_timeup(data_stream, timeleft):
        data_stream.putint(message_types.N_TIMEUP)
        data_stream.putint(timeleft)

    @staticmethod
    def put_pausegame(data_stream, paused, client=None):
        data_stream.putint(message_types.N_PAUSEGAME)
        data_stream.putint(paused)
        data_stream.putint(client.cn if client is not None else -1)

    @staticmethod
    def put_spectator(data_stream, player):
        data_stream.putint(message_types.N_SPECTATOR)
        data_stream.putint(player.pn)
        data_stream.putint(1 if player.state.is_spectator else 0)

    @staticmethod
    def put_setteam(data_stream, client, reason):
        data_stream.putint(message_types.N_SETTEAM)
        data_stream.putint(client.cn)
        data_stream.putstring(client.team.name)
        data_stream.putint(reason)

    @staticmethod
    def put_initai(data_stream, aiclient):
        data_stream.putint(message_types.N_INITAI)
        data_stream.putint(aiclient.cn)
        data_stream.putint(aiclient.owner.cn)
        data_stream.putint(aiclient.aitype)
        data_stream.putint(aiclient.aiskill)
        data_stream.putint(aiclient.playermodel)
        data_stream.putstring(aiclient.name)
        data_stream.putstring(aiclient.team)

    @staticmethod
    def put_initclient(data_stream, client):
        data_stream.putint(message_types.N_INITCLIENT)
        data_stream.putint(client.cn)
        data_stream.putstring(client.name)
        data_stream.putstring(client.team.name if client.team is not None else "")
        data_stream.putint(client.playermodel)

    @staticmethod
    def put_initclients(data_stream, clients):
        for client in clients:
            if client.isai:
                swh.put_initai(data_stream, client)
            else:
                swh.put_initclient(data_stream, client)

    @staticmethod
    def put_state(data_stream, player_state):
        data_stream.putint(player_state.lifesequence)
        data_stream.putint(player_state.health)
        data_stream.putint(player_state.maxhealth)
        data_stream.putint(player_state.armour)
        data_stream.putint(player_state.armourtype)
        data_stream.putint(player_state.gunselect)

    @staticmethod
    def put_ammo(data_stream, player_state):
        for ammo_slot in player_state.ammo[weapon_types.GUN_SG:weapon_types.GUN_PISTOL + 1]:
            data_stream.putint(ammo_slot)

    @staticmethod
    def put_resume(data_stream, players):
        data_stream.putint(message_types.N_RESUME)
        for player in players:
            data_stream.putint(player.pn)
            data_stream.putint(player.state.state)
            data_stream.putint(player.state.frags)
            data_stream.putint(player.state.flags)
            data_stream.putint(player.state.quadremaining)

            swh.put_state(data_stream, player.state)
            swh.put_ammo(data_stream, player.state)

        data_stream.putint(-1)

    @staticmethod
    def put_itemacc(data_stream, item, client):
        data_stream.putint(message_types.N_ITEMACC)
        data_stream.putint(item.index)
        data_stream.putint(client.cn)

    @staticmethod
    def put_announce(data_stream, item):
        data_stream.putint(message_types.N_ANNOUNCE)
        data_stream.putint(item.type)

    @staticmethod
    def put_itemspawn(data_stream, item):
        data_stream.putint(message_types.N_ITEMSPAWN)
        data_stream.putint(item.index)

    @staticmethod
    def put_itemlist(data_stream, items):
        data_stream.putint(message_types.N_ITEMLIST)
        for item in items:
            if item.spawned:
                data_stream.putint(item.index)
                data_stream.putint(item.type)
        data_stream.putint(-1)

    @staticmethod
    def put_teaminfo(data_stream, teams):
        data_stream.putint(message_types.N_TEAMINFO)
        for team in teams:
            data_stream.putstring(team.name)
            data_stream.putint(team.frags)
        data_stream.putstring('')

    @staticmethod
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

    @staticmethod
    def put_dropflag(data_stream, client, flag):
        data_stream.putint(message_types.N_DROPFLAG)
        data_stream.putint(client.cn)
        data_stream.putint(flag.id)
        data_stream.putint(flag.version)
        data_stream.putint(flag.drop_location.x)
        data_stream.putint(flag.drop_location.y)
        data_stream.putint(flag.drop_location.z)

    @staticmethod
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

    @staticmethod
    def put_returnflag(data_stream, client, flag):
        data_stream.putint(message_types.N_RETURNFLAG)
        data_stream.putint(client.cn)
        data_stream.putint(flag.id)
        data_stream.putint(flag.version)

    @staticmethod
    def put_takeflag(data_stream, client, flag):
        data_stream.putint(message_types.N_TAKEFLAG)
        data_stream.putint(client.cn)
        data_stream.putint(flag.id)
        data_stream.putint(flag.version)

    @staticmethod
    def put_resetflag(data_stream, flag, team):
        data_stream.putint(message_types.N_RESETFLAG)
        data_stream.putint(flag.id)
        data_stream.putint(flag.version)
        data_stream.putint(flag.spawn)
        data_stream.putint(team.id)
        data_stream.putint(team.score)

    @staticmethod
    def put_invisflag(data_stream, flag):
        data_stream.putint(message_types.N_INVISFLAG)
        data_stream.putint(flag.id)
        data_stream.putint(flag.invisible)

    @staticmethod
    def put_bases(data_stream, bases):
        data_stream.putint(message_types.N_BASES)
        data_stream.putint(len(bases))
        for base in bases:
            data_stream.putint(base.ammotype)
            data_stream.putstring(base.ownerteam.name if base.ownerteam is not None else "")
            data_stream.putstring(base.enemyteam.name if base.enemyteam is not None else "")
            data_stream.putint(base.converted)
            data_stream.putint(base.ammocount)

    @staticmethod
    def put_baseinfo(data_stream, base):
        data_stream.putint(message_types.N_BASEINFO)
        data_stream.putint(base.id)
        data_stream.putstring(base.ownerteam.name if base.ownerteam is not None else "")
        data_stream.putstring(base.enemyteam.name if base.enemyteam is not None else "")
        data_stream.putint(base.converted)
        data_stream.putint(base.ammocount)
    
    @staticmethod
    def put_basescore(data_stream, base):
        data_stream.putint(message_types.N_BASESCORE)
        data_stream.putint(base.id)
        data_stream.putstring(base.ownerteam.name)
        data_stream.putint(base.ownerteam.score)

    @staticmethod
    def put_repammo(data_stream, client, base):
        data_stream.putint(message_types.N_REPAMMO)
        data_stream.putint(client.cn)
        data_stream.putint(base.ammotype)

    @staticmethod
    def put_baseregen(data_stream, client, base):
        data_stream.putint(message_types.N_BASEREGEN)
        data_stream.putint(client.cn)
        data_stream.putint(client.state.health)
        data_stream.putint(client.state.armour)
        data_stream.putint(base.ammotype)
        data_stream.putint(client.state.ammo[base.ammotype])

    @staticmethod
    def put_cdis(data_stream, client):
        data_stream.putint(message_types.N_CDIS)
        data_stream.putint(client.cn)

    @staticmethod
    def put_died(data_stream, client, killer):
        data_stream.putint(message_types.N_DIED)
        data_stream.putint(client.cn)
        data_stream.putint(killer.cn)
        data_stream.putint(killer.state.frags)
        if killer.team is not None:
            data_stream.putint(killer.team.frags)
        else:
            data_stream.putint(0)

    @staticmethod
    def put_forcedeath(data_stream, client):
        data_stream.putint(message_types.N_FORCEDEATH)
        data_stream.putint(client.cn)

    @staticmethod
    def put_jumppad(data_stream, client, jumppad):
        data_stream.putint(message_types.N_JUMPPAD)
        data_stream.putint(client.cn)
        data_stream.putint(jumppad)

    @staticmethod
    def put_teleport(data_stream, client, teleport, teledest):
        data_stream.putint(message_types.N_TELEPORT)
        data_stream.putint(client.cn)
        data_stream.putint(teleport)
        data_stream.putint(teledest)

    @staticmethod
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

    @staticmethod
    def put_explodefx(data_stream, client, gun, explode_id):
        data_stream.putint(message_types.N_EXPLODEFX)
        data_stream.putint(client.cn)
        data_stream.putint(gun)
        data_stream.putint(explode_id)

    @staticmethod
    def put_damage(data_stream, target, client, damage):
        data_stream.putint(message_types.N_DAMAGE)
        data_stream.putint(target.cn)
        data_stream.putint(client.cn)
        data_stream.putint(damage)
        data_stream.putint(target.state.armour)
        data_stream.putint(target.state.health)

    @staticmethod
    def put_hitpush(data_stream, target, gun, damage, v):
        data_stream.putint(message_types.N_HITPUSH)
        data_stream.putint(target.cn)
        data_stream.putint(gun)
        data_stream.putint(damage)
        data_stream.putint(v.x)
        data_stream.putint(v.y)
        data_stream.putint(v.z)

    @staticmethod
    def put_spawnstate(data_stream, player):
        data_stream.putint(message_types.N_SPAWNSTATE)
        data_stream.putint(player.pn)
        swh.put_state(data_stream, player.state)
        swh.put_ammo(data_stream, player.state)

    @staticmethod
    def put_spawn(data_stream, player_state):
        data_stream.putint(message_types.N_SPAWN)
        swh.put_state(data_stream, player_state)
        swh.put_ammo(data_stream, player_state)

    @staticmethod
    def put_pong(data_stream, cmillis):
        data_stream.putint(message_types.N_PONG)
        data_stream.putint(cmillis)

    @staticmethod
    def put_clientping(data_stream, ping):
        data_stream.putint(message_types.N_CLIENTPING)
        data_stream.putint(ping)

    @staticmethod
    def put_switchname(data_stream, name):
        data_stream.putint(message_types.N_SWITCHNAME)
        data_stream.putstring(name)

    @staticmethod
    def put_switchmodel(data_stream, playermodel):
        data_stream.putint(message_types.N_SWITCHMODEL)
        data_stream.putint(playermodel)

    @staticmethod
    def put_taunt(data_stream):
        data_stream.putint(message_types.N_TAUNT)

    @staticmethod
    def put_gunselect(data_stream, gunselect):
        data_stream.putint(message_types.N_GUNSELECT)
        data_stream.putint(gunselect)

    @staticmethod
    def put_sound(data_stream, sound):
        data_stream.putint(message_types.N_SOUND)
        data_stream.putint(sound)

    @staticmethod
    def put_clientdata(data_stream, client, data):
        data_stream.putint(message_types.N_CLIENT)
        data_stream.putint(client.cn)
        data_stream.putuint(len(data))
        data_stream.write(data)

    @staticmethod
    def put_text(data_stream, text):
        data_stream.putint(message_types.N_TEXT)
        data_stream.putstring(text)

    @staticmethod
    def put_sayteam(data_stream, client, text):
        data_stream.putint(message_types.N_SAYTEAM)
        data_stream.putint(client.cn)
        data_stream.putstring(text)

    @staticmethod
    def put_authchall(data_stream, desc, auth_id, challenge):
        data_stream.putint(message_types.N_AUTHCHAL)
        data_stream.putstring(desc)
        data_stream.putint(auth_id)
        data_stream.putstring(challenge)

    @staticmethod
    def put_newmap(data_stream, size):
        data_stream.putint(message_types.N_NEWMAP)
        data_stream.putint(size)

    @staticmethod
    def put_vector(data_stream, v):
        data_stream.putint(v.x)
        data_stream.putint(v.y)
        data_stream.putint(v.z)

    @staticmethod
    def put_editmode(data_stream, editmode):
        data_stream.putint(message_types.N_EDITMODE)
        data_stream.putint(1 if editmode else 0)

    @staticmethod
    def put_editent(data_stream, ent_id, v, ent_type, attrs):
        assert(len(attrs) == 5)
        data_stream.putint(message_types.N_EDITENT)
        data_stream.putint(ent_id)
        swh.put_vector(data_stream, v)
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

    @staticmethod
    def put_editf(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner, move_dir, mode_mode):
        data_stream.putint(message_types.N_EDITF)

        swh.put_vector(data_stream, sel_o)
        swh.put_vector(data_stream, sel_s)

        data_stream.putint(sel_grid)
        data_stream.putint(sel_orient)

        data_stream.putint(sel_cx)
        data_stream.putint(sel_cxs)
        data_stream.putint(sel_cy)
        data_stream.putint(sel_cys)

        data_stream.putint(sel_corner)

        data_stream.putint(move_dir)
        data_stream.putint(mode_mode)

    @staticmethod
    def put_editt(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner, tex, allfaces):
        data_stream.putint(message_types.N_EDITT)

        swh.put_vector(data_stream, sel_o)
        swh.put_vector(data_stream, sel_s)

        data_stream.putint(sel_grid)
        data_stream.putint(sel_orient)

        data_stream.putint(sel_cx)
        data_stream.putint(sel_cxs)
        data_stream.putint(sel_cy)
        data_stream.putint(sel_cys)

        data_stream.putint(sel_corner)

        data_stream.putint(tex)
        data_stream.putint(allfaces)

    @staticmethod
    def put_delcube(data_stream, sel_o, sel_s, sel_grid, sel_orient, sel_cx, sel_cxs, sel_cy, sel_cys, sel_corner):
        data_stream.putint(message_types.N_DELCUBE)

        swh.put_vector(data_stream, sel_o)
        swh.put_vector(data_stream, sel_s)

        data_stream.putint(sel_grid)
        data_stream.putint(sel_orient)

        data_stream.putint(sel_cx)
        data_stream.putint(sel_cxs)
        data_stream.putint(sel_cy)
        data_stream.putint(sel_cys)

        data_stream.putint(sel_corner)
