import math

from cube2common.constants import RAD


def vectoyawpitch(v):
    yaw = -math.atan2(v.x, v.y)/RAD;
    vmag = v.magnitude()
    pitch = 0.0
    if vmag != 0:
        pitch = math.asin(v.z/vmag)/RAD
    return yaw, pitch