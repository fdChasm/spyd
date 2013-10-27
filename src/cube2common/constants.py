from cube2common.utils.enum import enum

MAPVERSION = 33
PROTOCOL_VERSION = 259

# match constants
INTERMISSIONLEN = 10
RESETFLAGTIME = 10000

# string length constants
MAXSERVERDESCLEN = 25
MAXSERVERLEN = 13
MAXNAMELEN = 15
MAXTEAMLEN = 4
MAXAUTHNAMELEN = 100
MAXROOMLEN = 7
AUTHCHALLEN = 49
AUTHANSLEN = 48
AUTHPUBKEYLEN = 48
AUTHPRIVKEYLEN = 49

# math constants
PI = 3.1415927
SQRT2 = 1.4142136
SQRT3 = 1.7320508
RAD = PI / 180.0

# network quantization scale
DMF = 16.0                # for world locations
DNF = 100.0               # for normalized vectors
DVELF = 1.0               # for playerspeed based velocity vectors

# weapon detail constants
MAXRAYS = 20
EXP_SELFDAMDIV = 2.0
EXP_SELFPUSH = 2.5
EXP_DISTSCALE = 1.5

# map file constants
MAXENTS = 10000

DEATHMILLIS = 300

base_entity_types = enum('ET_EMPTY', 'ET_LIGHT', 'ET_MAPMODEL', 'ET_PLAYERSTART', 'ET_ENVMAP', 'ET_PARTICLES', 'ET_SOUND', 'ET_SPOTLIGHT', 'ET_GAMESPECIFIC')

game_entity_types = enum(                     # static entity types
    'NOTUSED',                                  # entity slot not in use in map
    'LIGHT',                                    # lightsource, attr1 = radius, attr2 = intensity
    'MAPMODEL',                                 # attr1 = angle, attr2 = idx
    'PLAYERSTART',                              # attr1 = angle, attr2 = team
    'ENVMAP',                                   # attr1 = radius
    'PARTICLES',
    'MAPSOUND',
    'SPOTLIGHT',
    'I_SHELLS', 'I_BULLETS', 'I_ROCKETS', 'I_ROUNDS', 'I_GRENADES', 'I_CARTRIDGES',
    'I_HEALTH', 'I_BOOST',
    'I_GREENARMOUR', 'I_YELLOWARMOUR',
    'I_QUAD',
    'TELEPORT',                                 # attr1 = idx, attr2 = model, attr3 = tag
    'TELEDEST',                                 # attr1 = angle, attr2 = idx
    'MONSTER',                                  # attr1 = angle, attr2 = monstertype
    'CARROT',                                   # attr1 = tag, attr2 = type
    'JUMPPAD',                                  # attr1 = zpush, attr2 = ypush, attr3 = xpush
    'BASE',
    'RESPAWNPOINT',
    'BOX',                                      # attr1 = angle, attr2 = idx, attr3 = weight
    'BARREL',                                   # attr1 = angle, attr2 = idx, attr3 = weight, attr4 = health
    'PLATFORM',                                 # attr1 = angle, attr2 = idx, attr3 = tag, attr4 = speed
    'ELEVATOR',                                 # attr1 = angle, attr2 = idx, attr3 = tag, attr4 = speed
    'FLAG',                                     # attr1 = angle, attr2 = team
    'MAXENTTYPES')

# cubescript identity types
cs_id_types = enum('ID_VAR', 'ID_FVAR', 'ID_SVAR', 'ID_COMMAND', 'ID_CCOMMAND', 'ID_ALIAS')

client_states = enum('CS_ALIVE', 'CS_DEAD', 'CS_SPAWNING', 'CS_LAGGED', 'CS_EDITING', 'CS_SPECTATOR')

weapon_types = enum('GUN_FIST', 'GUN_SG', 'GUN_CG', 'GUN_RL', 'GUN_RIFLE', 'GUN_GL', 'GUN_PISTOL', 'GUN_FIREBALL', 'GUN_ICEBALL', 'GUN_SLIMEBALL', 'GUN_BITE', 'GUN_BARREL', 'NUMGUNS')

item_types = enum(  NOTUSED=0,
                    I_SHELLS=8, I_BULLETS=9, I_ROCKETS=10, I_ROUNDS=11, I_GRENADES=12, I_CARTRIDGES=13,
                    I_HEALTH=14, I_BOOST=15,
                    I_GREENARMOUR=16, I_YELLOWARMOUR=17,
                    I_QUAD=18)

shader_param_types = enum('SHPARAM_LOOKUP', 'SHPARAM_VERTEX', 'SHPARAM_PIXEL', 'SHPARAM_UNIFORM')
vslot_types = enum ('VSLOT_SHPARAM', 'VSLOT_SCALE', 'VSLOT_ROTATION', 'VSLOT_OFFSET', 'VSLOT_SCROLL', 'VSLOT_LAYER', 'VSLOT_ALPHA', 'VSLOT_COLOR', 'VSLOT_NUM')
octa_save_types = enum('OCTSAV_CHILDREN', 'OCTSAV_EMPTY', 'OCTSAV_SOLID', 'OCTSAV_NORMAL', 'OCTSAV_LODCUBE')

F_EMPTY = 0
F_SOLID = 0x80808080

material_types = enum(
    MATF_INDEX_SHIFT  = 0,
    MATF_VOLUME_SHIFT = 2,
    MATF_CLIP_SHIFT   = 5,
    MATF_FLAG_SHIFT   = 8,

    MATF_INDEX  = 3 << 0,    #MATF_INDEX_SHIFT
    MATF_VOLUME = 7 << 2,    #MATF_VOLUME_SHIFT
    MATF_CLIP   = 7 << 5,    #MATF_CLIP_SHIFT
    MATF_FLAGS  = 0xFF << 8) #MATF_FLAG_SHIFT

empty_material_types = enum( # cube empty-space materials
    MAT_AIR      = 0,                      # the default, fill the empty space with air
    MAT_WATER    = 1 << 2, #MATF_VOLUME_SHIFT, # fill with water, showing waves at the surface
    MAT_LAVA     = 2 << 2, #MATF_VOLUME_SHIFT, # fill with lava
    MAT_GLASS    = 3 << 2, #MATF_VOLUME_SHIFT, # behaves like clip but is blended blueish

    MAT_NOCLIP   = 1 << 5, #MATF_CLIP_SHIFT,  # collisions always treat cube as empty
    MAT_CLIP     = 2 << 5, #MATF_CLIP_SHIFT,  # collisions always treat cube as solid
    MAT_GAMECLIP = 3 << 5, #MATF_CLIP_SHIFT,  # game specific clip material

    MAT_DEATH    = 1 << 8, #MATF_FLAG_SHIFT,  # force player suicide
    MAT_ALPHA    = 4 << 8) #MATF_FLAG_SHIFT   # alpha blended

lighting_types = enum('LMID_AMBIENT', 'LMID_AMBIENT1', 'LMID_BRIGHT', 'LMID_BRIGHT1', 'LMID_DARK', 'LMID_DARK1', 'LMID_RESERVED')

layer_types = enum(
    LAYER_TOP    = (1<<5),
    LAYER_BOTTOM = (1<<6),
    LAYER_DUP    = (1<<7),

    LAYER_BLEND  = (1<<5)|(1<<6),#LAYER_TOP|LAYER_BOTTOM,
    
    MAXFACEVERTS = 15)

LM_PACKW = 512
LM_PACKH = 512
USHRT_MAX = 65535

hardcoded_textures = enum('DEFAULT_SKY', 'DEFAULT_GEOM') #hardcoded texture numbers

octsave = enum('OCTSAV_CHILDREN', 'OCTSAV_EMPTY', 'OCTSAV_SOLID', 'OCTSAV_NORMAL', 'OCTSAV_LODCUBE')

sounds = enum(
    'S_JUMP', 'S_LAND', 'S_RIFLE', 'S_PUNCH1', 'S_SG', 'S_CG',
    'S_RLFIRE', 'S_RLHIT', 'S_WEAPLOAD', 'S_ITEMAMMO', 'S_ITEMHEALTH',
    'S_ITEMARMOUR', 'S_ITEMPUP', 'S_ITEMSPAWN', 'S_TELEPORT', 'S_NOAMMO', 'S_PUPOUT',
    'S_PAIN1', 'S_PAIN2', 'S_PAIN3', 'S_PAIN4', 'S_PAIN5', 'S_PAIN6',
    'S_DIE1', 'S_DIE2',
    'S_FLAUNCH', 'S_FEXPLODE',
    'S_SPLASH1', 'S_SPLASH2',
    'S_GRUNT1', 'S_GRUNT2', 'S_RUMBLE',
    'S_PAINO',
    'S_PAINR', 'S_DEATHR',
    'S_PAINE', 'S_DEATHE',
    'S_PAINS', 'S_DEATHS',
    'S_PAINB', 'S_DEATHB',
    'S_PAINP', 'S_PIGGR2',
    'S_PAINH', 'S_DEATHH',
    'S_PAIND', 'S_DEATHD',
    'S_PIGR1', 'S_ICEBALL', 'S_SLIMEBALL',
    'S_JUMPPAD', 'S_PISTOL',

    'S_V_BASECAP', 'S_V_BASELOST',
    'S_V_FIGHT',
    'S_V_BOOST', 'S_V_BOOST10',
    'S_V_QUAD', 'S_V_QUAD10',
    'S_V_RESPAWNPOINT',

    'S_FLAGPICKUP',
    'S_FLAGDROP',
    'S_FLAGRETURN',
    'S_FLAGSCORE',
    'S_FLAGRESET',

    'S_BURN',
    'S_CHAINSAW_ATTACK',
    'S_CHAINSAW_IDLE',

    'S_HIT',
    
    'S_FLAGFAIL')

class GunInfo(object):
    sound, attackdelay, damage, spread, projspeed, kickamount, gunrange, rays, hitpush, exprad, ttl = [0]*11
    
    def __init__(self, sound, attackdelay, damage, spread, projspeed, kickamount, gunrange, rays, hitpush, exprad, ttl, name):
        self.sound = sound
        self.attackdelay = float(attackdelay)
        self.damage = float(damage)
        self.spread = float(spread)
        self.projspeed = float(projspeed)
        self.kickamount = float(kickamount)
        self.range = float(gunrange)
        self.rays = float(rays)
        self.hitpush = float(hitpush)
        self.exprad = float(exprad)
        self.ttl = float(ttl)
        self.name = name

guns = [
    #       sound               attackdelay  damage spread    projspeed   kickamount  range  rays  hitpush   exprad   ttl    name
    GunInfo(sounds.S_PUNCH1,    250,         50,    0,        0,          0,          14,    1,    80,       0,       0,     "fist"),
    GunInfo(sounds.S_SG,        1400,        10,    400,      0,          20,         1024,  20,   80,       0,       0,     "shotgun"),
    GunInfo(sounds.S_CG,        100,         30,    100,      0,          7,          1024,  1,    80,       0,       0,     "chaingun"),
    GunInfo(sounds.S_RLFIRE,    800,         120,   0,        320,        10,         1024,  1,    160,      40,      0,     "rocketlauncher"),
    GunInfo(sounds.S_RIFLE,     1500,        100,   0,        0,          30,         2048,  1,    80,       0,       0,     "rifle"),
    GunInfo(sounds.S_FLAUNCH,   500,         90,    0,        200,        10,         1024,  1,    250,      45,      1500,  "grenadelauncher"),
    GunInfo(sounds.S_PISTOL,    500,         35,    50,       0,          7,          1024,  1,    80,       0,       0,     "pistol"),
    GunInfo(sounds.S_FLAUNCH,   200,         20,    0,        200,        1,          1024,  1,    80,       40,      0,     "fireball"),
    GunInfo(sounds.S_ICEBALL,   200,         40,    0,        120,        1,          1024,  1,    80,       40,      0,     "iceball"),
    GunInfo(sounds.S_SLIMEBALL, 200,         30,    0,        640,        1,          1024,  1,    80,       40,      0,     "slimeball"),
    GunInfo(sounds.S_PIGR1,     250,         50,    0,        0,          1,          12,    1,    80,       0,       0,     "bite"),
]

armor_types = enum('A_BLUE', 'A_GREEN', 'A_YELLOW')

class ItemStat(object):
    add, max, info = [0]*3

    def __init__(self, a, m, i=0):
        self.add = a
        self.max = m
        self.info = i

itemstats = [
    ItemStat(10,    30,    weapon_types.GUN_SG),
    ItemStat(20,    60,    weapon_types.GUN_CG),
    ItemStat(5,     15,    weapon_types.GUN_RL),
    ItemStat(5,     15,    weapon_types.GUN_RIFLE),
    ItemStat(10,    30,    weapon_types.GUN_GL),
    ItemStat(30,    120,   weapon_types.GUN_PISTOL),
    ItemStat(25,    100),
    ItemStat(10,    1000),
    ItemStat(100,   100,   armor_types.A_GREEN),
    ItemStat(200,   200,   armor_types.A_YELLOW),
    ItemStat(20000, 30000),
]

privileges = enum('PRIV_NONE', 'PRIV_MASTER', 'PRIV_AUTH', 'PRIV_ADMIN')

mastermodes = enum('MM_OPEN', 'MM_VETO', 'MM_LOCKED', 'MM_PRIVATE', 'MM_PASSWORD', MM_AUTH=-1)

disconnect_types = enum('DISC_NONE', 'DISC_EOP', 'DISC_LOCAL', 'DISC_KICK', 'DISC_MSGERR', 'DISC_IPBAN', 'DISC_PRIVATE', 'DISC_MAXCLIENTS', 'DISC_TIMEOUT', 'DISC_OVERFLOW', 'DISC_PASSWORD', 'DISC_NUM')

message_types = enum('N_CONNECT', 'N_SERVINFO', 'N_WELCOME', 'N_INITCLIENT', 'N_POS', 'N_TEXT', 'N_SOUND', 'N_CDIS',
                     'N_SHOOT', 'N_EXPLODE', 'N_SUICIDE',
                     'N_DIED', 'N_DAMAGE', 'N_HITPUSH', 'N_SHOTFX', 'N_EXPLODEFX',
                     'N_TRYSPAWN', 'N_SPAWNSTATE', 'N_SPAWN', 'N_FORCEDEATH',
                     'N_GUNSELECT', 'N_TAUNT',
                     'N_MAPCHANGE', 'N_MAPVOTE', 'N_TEAMINFO', 'N_ITEMSPAWN', 'N_ITEMPICKUP', 'N_ITEMACC', 'N_TELEPORT', 'N_JUMPPAD',
                     'N_PING', 'N_PONG', 'N_CLIENTPING',
                     'N_TIMEUP', 'N_FORCEINTERMISSION',
                     'N_SERVMSG', 'N_ITEMLIST', 'N_RESUME',
                     'N_EDITMODE', 'N_EDITENT', 'N_EDITF', 'N_EDITT', 'N_EDITM', 'N_FLIP', 'N_COPY', 'N_PASTE', 'N_ROTATE', 'N_REPLACE', 'N_DELCUBE', 'N_REMIP', 'N_NEWMAP', 'N_GETMAP', 'N_SENDMAP', 'N_CLIPBOARD', 'N_EDITVAR',
                     'N_MASTERMODE', 'N_KICK', 'N_CLEARBANS', 'N_CURRENTMASTER', 'N_SPECTATOR', 'N_SETMASTER', 'N_SETTEAM',
                     'N_BASES', 'N_BASEINFO', 'N_BASESCORE', 'N_REPAMMO', 'N_BASEREGEN', 'N_ANNOUNCE',
                     'N_LISTDEMOS', 'N_SENDDEMOLIST', 'N_GETDEMO', 'N_SENDDEMO',
                     'N_DEMOPLAYBACK', 'N_RECORDDEMO', 'N_STOPDEMO', 'N_CLEARDEMOS',
                     'N_TAKEFLAG', 'N_RETURNFLAG', 'N_RESETFLAG', 'N_INVISFLAG', 'N_TRYDROPFLAG', 'N_DROPFLAG', 'N_SCOREFLAG', 'N_INITFLAGS',
                     'N_SAYTEAM',
                     'N_CLIENT',
                     'N_AUTHTRY', 'N_AUTHKICK', 'N_AUTHCHAL', 'N_AUTHANS', 'N_REQAUTH',
                     'N_PAUSEGAME', 'N_GAMESPEED',
                     'N_ADDBOT', 'N_DELBOT', 'N_INITAI', 'N_FROMAI', 'N_BOTLIMIT', 'N_BOTBALANCE',
                     'N_MAPCRC', 'N_CHECKMAPS',
                     'N_SWITCHNAME', 'N_SWITCHMODEL', 'N_SWITCHTEAM',
                     'N_INITTOKENS', 'N_TAKETOKEN', 'N_EXPIRETOKENS', 'N_DROPTOKENS', 'N_DEPOSITTOKENS', 'N_STEALTOKENS',
                     'N_SERVCMD',
                     'N_DEMOPACKET',
                     'NUMMSG')

INT_MAX = (2**32)-1
