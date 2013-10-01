'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.utils import readuchar

class MergesCompat(object):
    u1 = 0
    u2 = 0
    v1 = 0
    v2 = 0
    
    @staticmethod
    def read(f):
        mc = MergesCompat()
        mc.u1 = readuchar(f)
        mc.u2 = readuchar(f)
        mc.v1 = readuchar(f)
        mc.v2 = readuchar(f)
        return mc