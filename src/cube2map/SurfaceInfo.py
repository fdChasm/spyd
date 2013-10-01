'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.constants import layer_types
from cube2map.utils import readuchar
import struct

class SurfaceInfo(object):
    lmid = [0]*2
    verts = 0
    numverts = 0
    
    @staticmethod
    def read(f):
        si = SurfaceInfo()
        si.lmid = struct.unpack("2B", f.read(2))
        si.verts = readuchar(f)
        si.numverts = readuchar(f)
        return si
    
    @property
    def totalverts(self):
        if self.numverts & layer_types.LAYER_DUP:
            return (self.numverts & layer_types.MAXFACEVERTS)*2
        else:
            return (self.numverts & layer_types.MAXFACEVERTS)
        
    def __eq__(self, o):
        return self.lmid[0] == o.lmid[0] and self.lmid[1] == o.lmid[1] and self.verts == o.verts and self.numverts == o.numverts