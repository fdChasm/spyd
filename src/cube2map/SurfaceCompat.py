'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
import struct
from cube2map.utils import readuchar, readushort

class SurfaceCompat(object):
    texcoords = [0]*8
    w = 0
    h = 0
    x = 0
    y = 0
    lmid = 0
    layer = 0
    
    @staticmethod
    def read(f):
        sc = SurfaceCompat()
        sc.texcoords = struct.unpack("8C", f.read(8))
        
        sc.w = readuchar(f)
        sc.h = readuchar(f)
        
        sc.x = readushort(f)
        sc.y = readushort(f)

        sc.lmid = readuchar(f)
        sc.layer = readuchar(f)
        
        return sc
    
    def compare_textcoords(self, other):
        i = 0
        while i < len(other.texcoords):
            if self.texcoords[i] != other.texcoords[i]:
                return False
        return True