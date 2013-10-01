'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.constants import RAD
from cube2map.utils import ushort, clamp
import math

def encodenormal(n):
    if n.iszero():
        return 0
    
    yaw = int(-math.atan2(n.x, n.y)/RAD)
    pitch = int(math.asin(n.z)/RAD)
    
    if yaw < 0:
        v = yaw%360 + 360
    else:
        v = yaw%360
    
    return ushort(clamp(pitch + 90, 0, 180)*360 + v + 1);