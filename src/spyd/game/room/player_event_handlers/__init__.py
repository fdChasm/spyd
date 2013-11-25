from cube2common.constants import weapon_types, client_states
from cube2common.cube_data_stream import CubeDataStream
from spyd.protocol import swh
from spyd.registry_manager import register
from spyd.utils.constrain import constrain_range


@register('room_player_event_handler')
class switch_modelHandler(object):
    event_type = 'switch_model'

    @staticmethod
    def handle(room, player, playermodel):
        constrain_range(playermodel, 0, 4, "playermodels")
        player.playermodel = playermodel
        swh.put_switchmodel(player.state.messages, playermodel)

@register('room_player_event_handler')
class switch_nameHandler(object):
    event_type = 'switch_name'

    @staticmethod
    def handle(room, player, name):
        player.name = name
        swh.put_switchname(player.state.messages, name)
        # with room.broadcastbuffer(1, True) as cds:
        #    tm = CubeDataStream()
        #    swh.put_switchname(tm, "aaaaa")
        #    swh.put_clientdata(cds, player.client, str(tm))

@register('room_player_event_handler')
class switch_teamHandler(object):
    event_type = 'switch_team'

    @staticmethod
    def handle(room, player, team_name):
        room.gamemode.on_player_try_set_team(player, player, player.team.name, team_name)

@register('room_player_event_handler')
class tauntHandler(object):
    event_type = 'taunt'

    @staticmethod
    def handle(room, player):
        room.gamemode.on_player_taunt(player)

@register('room_player_event_handler')
class teleportHandler(object):
    event_type = 'teleport'

    @staticmethod
    def handle(room, player, teleport, teledest):
        room._broadcaster.teleport(player, teleport, teledest)

@register('room_player_event_handler')
class jumppadHandler(object):
    event_type = 'jumppad'

    @staticmethod
    def handle(room, player, jumppad):
        room._broadcaster.jumppad(player, jumppad)

@register('room_player_event_handler')
class suicideHandler(object):
    event_type = 'suicide'

    @staticmethod
    def handle(room, player):
        player.state.state = client_states.CS_DEAD
        room.gamemode.on_player_death(player, player)
        room._broadcaster.player_died(player, player)


@register('room_player_event_handler')
class shootHandler(object):
    event_type = 'shoot'

    @staticmethod
    def handle(room, player, shot_id, gun, from_pos, to_pos, hits):
        constrain_range(gun, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        room.gamemode.on_player_shoot(player, shot_id, gun, from_pos, to_pos, hits)

@register('room_player_event_handler')
class explodeHandler(object):
    event_type = 'explode'

    @staticmethod
    def handle(room, player, cmillis, gun, explode_id, hits):
        constrain_range(gun, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        room.gamemode.on_player_explode(player, cmillis, gun, explode_id, hits)

@register('room_player_event_handler')
class request_spawnHandler(object):
    event_type = 'request_spawn'

    @staticmethod
    def handle(room, player):
        room.gamemode.on_player_request_spawn(player)

@register('room_player_event_handler')
class spawnHandler(object):
    event_type = 'spawn'

    @staticmethod
    def handle(room, player, lifesequence, gunselect):
        constrain_range(gunselect, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        player.state.on_respawn(lifesequence, gunselect)

@register('room_player_event_handler')
class gunselectHandler(object):
    event_type = 'gunselect'

    @staticmethod
    def handle(room, player, gunselect):
        constrain_range(gunselect, weapon_types.GUN_FIST, weapon_types.GUN_PISTOL, "weapon_types")
        player.state.gunselect = gunselect
        swh.put_gunselect(player.state.messages, gunselect)

@register('room_player_event_handler')
class soundHandler(object):
    event_type = 'sound'

    @staticmethod
    def handle(room, player, sound):
        swh.put_sound(player.state.messages, sound)

@register('room_player_event_handler')
class pickup_itemHandler(object):
    event_type = 'pickup_item'

    @staticmethod
    def handle(room, player, item_index):
        room.gamemode.on_player_pickup_item(player, item_index)

@register('room_player_event_handler')
class replenish_ammoHandler(object):
    event_type = 'replenish_ammo'

    @staticmethod
    def handle(room, player):
        pass

@register('room_player_event_handler')
class take_flagHandler(object):
    event_type = 'take_flag'

    @staticmethod
    def handle(room, player, flag, version):
        room.gamemode.on_player_take_flag(player, flag, version)


@register('room_player_event_handler')
class try_drop_flagHandler(object):
    event_type = 'try_drop_flag'

    @staticmethod
    def handle(room, player):
        room.gamemode.on_player_try_drop_flag(player)

@register('room_player_event_handler')
class game_chatHandler(object):
    event_type = 'game_chat'

    @staticmethod
    def handle(room, player, text):
        if text[0] == "#":
            room.command_executer.execute(room, player.client, text)
        else:
            swh.put_text(player.state.messages, text)
            room.event_subscription_fulfiller.publish('spyd.game.player.chat', {'player': player.uuid, 'room': room.name, 'text': text, 'scope': 'room'})

@register('room_player_event_handler')
class team_chatHandler(object):
    event_type = 'team_chat'

    @staticmethod
    def handle(room, player, text):
        if player.isai: return
        clients = filter(lambda c: c.get_player().team == player.team, room.clients)
        with room.broadcastbuffer(1, True, [player.client], clients) as cds:
            swh.put_sayteam(cds, player.client, text)
        room.event_subscription_fulfiller.publish('spyd.game.player.chat', {'player': player.uuid, 'room': room.name, 'text': text, 'scope': 'team'})

@register('room_player_event_handler')
class edit_modeHandler(object):
    event_type = 'edit_mode'

    @staticmethod
    def handle(room, player, editmode):
        with room.broadcastbuffer(1, True, [player]) as cds:
            tm = CubeDataStream()
            swh.put_editmode(tm, editmode)
            swh.put_clientdata(cds, player.client, str(tm))

@register('room_player_event_handler')
class edit_entityHandler(object):
    event_type = 'edit_entity'

    @staticmethod
    def handle(room, player, entity_id, entity_type, x, y, z, attrs):
        pass

@register('room_player_event_handler')
class edit_faceHandler(object):
    event_type = 'edit_face'

    @staticmethod
    def handle(room, selection, direction, mode):
        pass

@register('room_player_event_handler')
class edit_materialHandler(object):
    event_type = 'edit_material'

    @staticmethod
    def handle(room, selection, material, material_filter):
        pass

@register('room_player_event_handler')
class edit_textureHandler(object):
    event_type = 'edit_texture'

    @staticmethod
    def handle(room, selection, texture, all_faces):
        pass

@register('room_player_event_handler')
class edit_copyHandler(object):
    event_type = 'edit_copy'

    @staticmethod
    def handle(room, selection):
        pass

@register('room_player_event_handler')
class edit_pasteHandler(object):
    event_type = 'edit_paste'

    @staticmethod
    def handle(room, selection):
        pass

@register('room_player_event_handler')
class edit_flipHandler(object):
    event_type = 'edit_flip'

    @staticmethod
    def handle(room, selection):
        pass

@register('room_player_event_handler')
class edit_delete_cubesHandler(object):
    event_type = 'edit_delete_cubes'

    @staticmethod
    def handle(room, selection):
        pass

@register('room_player_event_handler')
class edit_rotateHandler(object):
    event_type = 'edit_rotate'

    @staticmethod
    def handle(room, selection, axis):
        pass

@register('room_player_event_handler')
class edit_replaceHandler(object):
    event_type = 'edit_replace'

    @staticmethod
    def handle(room, selection, texture, new_texture, in_selection):
        pass

