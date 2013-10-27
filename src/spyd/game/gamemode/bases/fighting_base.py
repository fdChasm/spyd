from cube2common.constants import DMF, weapon_types, guns, EXP_DISTSCALE, EXP_SELFDAMDIV, DNF, client_states, \
    DEATHMILLIS
from cube2common.vec import vec
from spyd.protocol import swh
from spyd.game.timing.expiry import Expiry


class FightingBase(object):
    def __init__(self, room, map_meta_data):
        self.room = room
        self._broadcaster = room._broadcaster
        self._game_clock = room._game_clock
    
    def on_player_shoot(self, player, shot_id, gun, from_pos, to_pos, hits):
        if not player.state.can_shoot: return

        pfrom = from_pos.copy().div(DMF)
        pto = to_pos.copy().div(DMF)

        if not player.state.check_alive(threshold=DEATHMILLIS): return
        if gun < weapon_types.GUN_FIST or gun > weapon_types.GUN_PISTOL: return
        if player.state.ammo[gun] <= 0: return
        if guns[gun].range and (pfrom.dist(pto) > guns[gun].range + 1): return

        if gun != weapon_types.GUN_FIST:
            player.state.ammo[gun] -= 1

        player.state.shotwait = Expiry(self._game_clock, float(guns[gun].attackdelay) / 1000.0)

        self._broadcaster.shotfx(player, gun, shot_id, from_pos, to_pos)

        player.state.damage_spent += guns[gun].damage * player.state.quad_multiplier * guns[gun].rays

        if gun == weapon_types.GUN_RL:
            player.state.rockets[shot_id] = gun
        elif gun == weapon_types.GUN_GL:
            player.state.grenades[shot_id] = gun
        else:
            total_rays = 0
            max_rays = guns[gun].rays
            for hit in hits:
                total_rays += hit['rays']
                if total_rays > max_rays: return
                self._on_player_hit(player, gun, **hit)
                
    def on_player_explode(self, player, cmillis, gun, explode_id, hits):
        if gun == weapon_types.GUN_RL:
            if not explode_id in player.state.rockets.keys(): return
            del player.state.rockets[explode_id]
        elif gun == weapon_types.GUN_GL:
            if not explode_id in player.state.grenades.keys(): return
            del player.state.grenades[explode_id]

        self._broadcaster.explodefx(player, gun, explode_id)

        for hit in hits:
            self._on_player_hit(player, gun, **hit)
            
    def _on_player_hit(self, player, gun, target_cn, lifesequence, distance, rays, dx, dy, dz):

        target = self.room.get_player(target_cn)

        if target is None: return

        damage = guns[gun].damage

        if not gun in [weapon_types.GUN_RL, weapon_types.GUN_GL]:
            damage *= rays

        damage *= player.state.quad_multiplier

        if gun in (weapon_types.GUN_RL, weapon_types.GUN_GL):
            damage *= (1.0 - ((distance / DMF) / EXP_DISTSCALE) / guns[gun].exprad)

            if target == player:
                damage /= EXP_SELFDAMDIV

        player.state.damage_dealt += int(damage)

        self._on_player_damaged(target, player, damage, gun, dx, dy, dz)

    def _on_player_damaged(self, target, player, damage, gun, dx, dy, dz):
        v = vec(dx, dy, dz).div(DMF).rescale(DNF)

        target.state.receive_damage(damage)

        with self.room.broadcastbuffer(1, True) as cds:
            swh.put_damage(cds, target, player, damage)

            if target == player:
                pass
            elif not v.iszero():
                if target.state.health <= 0:
                    swh.put_hitpush(cds, target, gun, damage, v)
                else:
                    with target.sendbuffer(1, True) as cds:
                        swh.put_hitpush(cds, target, gun, damage, v)

            if target.state.health < 1:
                target.state.state = client_states.CS_DEAD

                target.state.deaths += 1
                if player == target:
                    player.state.suicides += 1

                if self.hasteams and player.team == target.team:
                    player.state.teamkills += 1

                if player == target or self.hasteams and player.team == target.team:
                    mod = -1
                else:
                    mod = 1

                player.state.frags += mod
                if self.hasteams:
                    player.team.frags += mod

                swh.put_died(cds, target, player)

                self.on_player_death(target, player)
