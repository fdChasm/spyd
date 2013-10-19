import random
import traceback

from twisted.internet import reactor

from cube2common.constants import weapon_types, armor_types, DMF, guns, EXP_SELFDAMDIV, EXP_DISTSCALE, DNF, client_states
from cube2common.utils.enum import enum
from cube2common.vec import vec
from spyd.game.gamemode.bases.fighting_base import FightingBase
from spyd.game.gamemode.bases.mode_base import ModeBase
from spyd.game.gamemode.bases.spawning_base import SpawningBase
from spyd.game.gamemode.bases.spectating_base import SpectatingBase
from spyd.game.server_message_formatter import info
from spyd.game.timing.expiry import Expiry
from spyd.protocol import swh
from spyd.registry_manager import register


tist_states = enum('UNINITIALIZED', 'WAITING_PLAYERS', 'WAITING_TRAITOR', 'PLAYING')

@register('gamemode')
class Traitors(ModeBase, FightingBase, SpawningBase, SpectatingBase):
    isbasemode = False
    clientmodename = 'traitors'
    clientmodenum = 3
    timed = False
    timeout = 0
    hasitems = False
    hasflags = False
    hasteams = False
    hasbases = False
    spawnarmour = 0
    spawnarmourtype = armor_types.A_BLUE
    spawnhealth = 1
    spawndelay = 0

    min_players = 2

    @property
    def spawnammo(self):
        ammo = [0] * weapon_types.NUMGUNS
        ammo[weapon_types.GUN_FIST] = 1
        ammo[weapon_types.GUN_RIFLE] = 1337
        return ammo

    spawngunselect = weapon_types.GUN_RIFLE

    _tist_state = tist_states.UNINITIALIZED
    _tist_traitor_waiting_deferred = None
    _tist_intermission_end_deferred = None
    _tist_traitor = None

    def _start_info_message(self):
        self.room._broadcaster.server_message(info('Welcome to the Trouble in SauerTown gamemode. The first player to press their taunt bind will be the traitor.'))
        self.room._broadcaster.server_message(info('If no players do this a traitor will be selected at random in 5 seconds.'))

    def _waiting_players_message(self):
        deficit = self.min_players - self.room.playing_count
        format_args = {
                       'min_players': self.min_players,
                       'deficit': deficit,
                       'pl': 's' if deficit > 1 else '',
                       }
        self.room._broadcaster.server_message(info('The Trouble in SauerTown gamemode must be played with at least {min_players} players. Waiting for {deficit} more player{pl}.'.format(**format_args)))

    def _start_tist(self):
        self._start_info_message()
        self._tist_state = tist_states.WAITING_TRAITOR
        self._tist_traitor_waiting_deferred = self.room._game_clock.schedule_callback(5)
        self._tist_traitor_waiting_deferred.addCallback(self._waiting_traitor_timeout)

    def _waiting_traitor_timeout(self, *args):
        traitor = random.choice(list(self.room.players))
        self._select_traitor(traitor)

    def on_player_taunt(self, player):
        if self._tist_state == tist_states.WAITING_TRAITOR:
            self._tist_traitor_waiting_deferred.cancel()
            self._select_traitor(player)
        else:
            ModeBase.on_player_taunt(self, player)

    def _select_traitor(self, player):
        self._tist_traitor = player
        self._tist_state = tist_states.PLAYING
        self.room._broadcaster.server_message(info('The traitor has been selected. Trust no one!'))
        player.client.send_server_message(info('You are the traitor! Go kill them all...sneakily.'))
        for player in self.room.players:
            ModeBase.on_player_request_spawn(self, player)
        self.room._broadcaster.sound(12)

    def initialize(self):
        '''
        Check if there are enough players here, if so then tell them how to proceed.
        Otherwise tell them that we are waiting for more players to join
        '''
        if self.room.playing_count >= self.min_players:
            self._start_tist()
        else:
            self._waiting_players_message()
            self._tist_state = tist_states.WAITING_PLAYERS

    def on_player_connected(self, player):
        if self._tist_state == tist_states.WAITING_PLAYERS:
            if self.room.playing_count >= self.min_players:
                self._start_tist()
            else:
                reactor.callLater(0, self._waiting_players_message)
                
    def on_player_disconnected(self, player):
        if self._tist_state == tist_states.WAITING_TRAITOR:
            if self.room.playing_count < self.min_players:
                self._tist_traitor_waiting_deferred.cancel()
                self._waiting_players_message()
        elif self._tist_state == tist_states.WAITING_PLAYERS:
            self._waiting_players_message()
        elif self._tist_state == tist_states.PLAYING:
            if player is self._tist_traitor:
                self.room._broadcaster.server_message(info('The traitor, {name#traitor}, has left the game.', traitor=player))
                self._ended()
            else:
                alive_non_traitorous_players = filter(lambda p: p.state.is_alive and p is not self._tist_traitor, self.room.players)
                
                if len(alive_non_traitorous_players) == 0:
                    self.room._broadcaster.server_message(info('The the last living innocent player, {name#player}, has left the game. The traitor, {name#traitor}, is victorious.', traitor=self._tist_traitor, player=player))

    def on_player_death(self, player, killer):
        if self._tist_state == tist_states.PLAYING:
            player.client.send_server_message(info('You have been betrayed, choose your friends more wisely.'))
    
            alive_non_traitorous_players = filter(lambda p: p.state.is_alive and p is not self._tist_traitor, self.room.players)
    
            if player is self._tist_traitor:
                if player is killer:
                    self.room._broadcaster.server_message(info('The traitor, {name#traitor}, has suicided.', traitor=player))
                else:
                    self.room._broadcaster.server_message(info('The traitor, {name#traitor}, has been put down by {name#killer}.', killer=killer, traitor=player))
                self._ended()
            else:
                if len(alive_non_traitorous_players) == 0:
                    if killer is self._tist_traitor:
                        self.room._broadcaster.server_message(info('The traitor, {name#traitor}, has slaughtered all the innocents, claiming victory.', traitor=killer))
                    else:
                        self.room._broadcaster.server_message(info('The last innocent has died. The traitor, {name#traitor}, is victorious.', traitor=killer))
                    self._ended()

        ModeBase.on_player_death(self, player, killer)

    def _ended(self):
        self.room._broadcaster.time_left(0)
        self._tist_intermission_end_deferred = self.room._game_clock.schedule_callback(10)
        self._tist_intermission_end_deferred.addCallback(self._intermission_end)
        
    def _intermission_end(self, *args, **kwargs):
        try:
            self.room.rotate_map_mode()
        except:
            traceback.print_exc()

    def on_player_request_spawn(self, player):
        if self._tist_state == tist_states.PLAYING:
            player.client.send_server_message(info('Please wait until the next round to spawn.'))
        else:
            ModeBase.on_player_request_spawn(self, player)

    def on_player_shoot(self, player, shot_id, gun, from_pos, to_pos, hits):
        if not player.state.can_shoot: return

        pfrom = from_pos.copy().div(DMF)
        pto = to_pos.copy().div(DMF)

        if not player.state.is_alive: return
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
            for hit in hits:
                self._on_player_hit(player, gun, **hit)

    def on_player_explode(self, player, cmillis, gun, explode_id, hits):
        if gun == weapon_types.GUN_RL:
            if not explode_id in player.state.rockets.keys(): return
            del player.state.rockets[explode_id]
        elif gun == weapon_types.GUN_GL:
            if not explode_id in player.state.grenades.keys(): return
            del player.state.grenades[explode_id]

        self._broadcaster.explodefx(player, gun, explode_id)

        max_rays = guns[gun].rays

        total_rays = 0

        for hit in hits:
            total_rays += hit['rays']
            if total_rays > max_rays:
                break
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

                swh.put_died(cds, target, target)

                self.on_player_death(target, player)
