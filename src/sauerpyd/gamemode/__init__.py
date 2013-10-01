from utils.import_all import import_all
import_all(__file__, 'sauerpyd.gamemode', ['__init__'])
from sauerpyd.registry_manager import RegistryManager


mode_nums = {}
gamemodes = {}

gamemode_objects = map(lambda a: a.registered_object, RegistryManager.get_registrations('gamemode'))

for gamemode_object in gamemode_objects:
    if gamemode_object.isbasemode:
        mode_nums[gamemode_object.clientmodenum] = gamemode_object.clientmodename

for gamemode_object in gamemode_objects:
    gamemodes[gamemode_object.clientmodename] = gamemode_object

def get_mode_name_from_num(mode_num):
    return mode_nums.get(mode_num, None)
