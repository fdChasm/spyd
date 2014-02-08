from cube2common.constants import client_states, weapon_types, armor_types, item_types, itemstats
from cube2common.vec import vec
from cube2protocol.cube_data_stream import CubeDataStream
from spyd.game.player.kpd import KPD
from spyd.game.timing.expiry import Expiry
from spyd.game.timing.timer import Timer
from spyd.protocol import swh


class PlayerState(object):
    def __init__(self):
        self.game_clock = None
        self.messages = CubeDataStream()
        self.state = -1
        self.reset()

    def use_game_clock(self, game_clock):
        self.game_clock = game_clock

    @property
    def has_quad(self):
        if self._quadexpiry is not None:
            return not self._quadexpiry.is_expired
        return False

    @property
    def quad_multiplier(self):
        if self.has_quad:
            return 4
        else:
            return 1

    @property
    def quadremaining(self):
        if self.has_quad:
            return self._quadexpiry.remaining
        else:
            return 0

    @property
    def can_shoot(self):
        if not self.is_alive:
            return False
        if self.shotwait is not None:
            return self.shotwait.is_expired
        return True

    @property
    def can_spawn(self):
        if self.is_spectator:
            return False
        if self.is_alive:
            return False
        if self._pending_spawn:
            return False
        if self.spawnwait is not None:
            return self.spawnwait.is_expired
        return True

    @property
    def kpd(self):
        return KPD(self.frags, self.deaths)

    @property
    def acc_formatted(self):
        acc = self.acc_percent
        if acc is Ellipsis:
            return "inf"
        else:
            return "{:.2f}%".format(acc)

    @property
    def acc_percent(self):
        if self.damage_spent == 0:
            return Ellipsis
        return (100 * self.damage_dealt) / self.damage_spent

    @property
    def time_playing_this_match(self):
        if self.playing_timer is not None:
            return self.playing_timer.time_elapsed
        else:
            return 0.0

    @property
    def is_alive(self):
        return self.state == client_states.CS_ALIVE

    @property
    def millis_since_death(self):
        if self.death_timer is None: return None
        return self.death_timer.time_elapsed * 1000

    def check_alive(self, threshold=None):
        if threshold is None: return self.is_alive
        if self.is_alive:
            return True
        else:
            millis_since_death = self.millis_since_death
            return millis_since_death is not None and millis_since_death < threshold

    @property
    def is_spectator(self):
        return self.state == client_states.CS_SPECTATOR

    @is_spectator.setter
    def is_spectator(self, value):
        if value and not self.is_spectator:
            self.state = client_states.CS_SPECTATOR
            if self.playing_timer is not None:
                self.playing_timer.pause()
        elif not value and self.is_spectator:
            self.state = client_states.CS_DEAD
            if self.playing_timer is not None:
                self.playing_timer.resume()
        else:
            print "failed to set is_spectator"

    def respawn(self, gamemode):
        self._pending_spawn = True
        self.lifesequence = (self.lifesequence + 1) & 0x7F
        self._quadexpiry = None
        self.health = gamemode.spawnhealth
        self.armour = gamemode.spawnarmour
        self.armourtype = gamemode.spawnarmourtype
        self.gunselect = gamemode.spawngunselect
        self.ammo = gamemode.spawnammo

        self.position = None

    def on_respawn(self, lifesequence, gunselect):
        if lifesequence != self.lifesequence: return
        self._pending_spawn = False
        self.state = client_states.CS_ALIVE
        self.gunselect = gunselect

        swh.put_spawn(self.messages, self)

    def update_position(self, position, raw_position):
        self.position = raw_position
        self.pos.v = position

    def clear_flushed_state(self):
        self.messages = CubeDataStream()
        self.position = None

    def map_change_reset(self):
        if self.state != client_states.CS_SPECTATOR:
            self.state = client_states.CS_DEAD

        self.frags = 0
        self.deaths = 0
        self.suicides = 0
        self.teamkills = 0
        self.damage_dealt = 0
        self.damage_spent = 0
        self.flags = 0
        self.flag_returns = 0
        self.health = 100
        self.maxhealth = 100
        self.armour = 0
        self.armourtype = armor_types.A_BLUE
        self.gunselect = weapon_types.GUN_PISTOL
        self.ammo = [0] * weapon_types.NUMGUNS

        if self.game_clock is not None:
            self.playing_timer = Timer(self.game_clock)
        else:
            self.playing_timer = None

        self.death_timer = None

        self.pos = vec(0, 0, 0)

        self._quadexpiry = None
        self.shotwait = None
        self.spawnwait = None
        self._pending_spawn = False

        self.rockets = {}
        self.grenades = {}

        self.messages.clear()
        self.position = None

    def reset(self):
        self.map_change_reset()
        self.state = client_states.CS_ALIVE
        self.lifesequence = -1

    def receive_damage(self, damage):
        # let armour absorb when possible
        ad = damage * (self.armourtype + 1) * (25.0 / 100.0)
        if ad > self.armour:
            ad = self.armour
        self.armour -= int(ad)
        damage = int(damage - int(ad))
        self.health -= damage
        return damage

    def suicide(self):
        self.frags -= 1
        self.deaths += 1
        self.suicides += 1
        self.state = client_states.CS_DEAD

    def died(self):
        if self.game_clock is not None:
            self.death_timer = Timer(self.game_clock)
        else:
            self.death_timer = None

    def pickup_item(self, item_type):
        if item_type < item_types.I_SHELLS or item_type > item_types.I_QUAD:
            print "Item out of range could not be picked up."
            return

        itemstat = itemstats[item_type - item_types.I_SHELLS]

        if item_type == item_types.I_BOOST:  # boost also adds to health
            if self.maxhealth >= itemstat.max: return False
            self.maxhealth = min(self.maxhealth + itemstat.add, itemstat.max)

        if item_type in (item_types.I_BOOST, item_types.I_HEALTH):
            self.health = min(self.health + itemstat.add, self.maxhealth)

        elif item_type in [item_types.I_GREENARMOUR, item_types.I_YELLOWARMOUR]:
            if self.armour >= itemstat.max: return False
            self.armour = min(self.armour + itemstat.add, itemstat.max)
            self.armourtype = itemstat.info

        elif item_type == item_types.I_QUAD:
            if self.has_quad:
                self._quadexpiry.extend(float(itemstat.add) / 1000.0, float(itemstat.max) / 1000.0)
            else:
                self._quadexpiry = Expiry(self.game_clock, float(itemstat.add) / 1000.0)

        else:  # is an ammo
            if self.ammo[itemstat.info] >= itemstat.max: return False
            self.ammo[itemstat.info] = min(self.ammo[itemstat.info] + itemstat.add, itemstat.max)

        return True
