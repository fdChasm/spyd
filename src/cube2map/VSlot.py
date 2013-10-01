#@PydevCodeAnalysisIgnore
'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.constants import shader_param_types, vslot_types
from cube2common.vec import vec
from cube2map.ShaderParam import ShaderParam
from cube2map.utils import readushort, readfloat, readint
import struct

class VSlot(object):
    def __init__(self, index):
        self.next = None
        self.index = index
        self.changed = 0
        self.skipped = 0

        self.params = []
        self.linked = False
        self.scale = 1;
        self.rotation = 0
        self.xoffset = 0
        self.yoffset = 0
        self.scrollS = 0
        self.scrollT = 0
        self.layer = 0
        self.alphafront = 0.5
        self.alphaback = 0
        self.colorscale = vec(1, 1, 1)
        self.glowcolor = vec(1, 1, 1)
        self.pulseglowcolor = vec(0, 0, 0)
        self.pulseglowspeed = 0
        self.envscale = vec(0, 0, 0)
        
def load_vslot(f, index, changed):
    vs = VSlot(index)
    numparams = readushort(f)
    for i in xrange(numparams):
        nlen = readushort(f)
        name = f.read(nlen)
        p = ShaderParam(name, shader_param_types.SHPARAM_LOOKUP)
        p.val = struct.unpack("4i", f.read(12))
        vs.params.append(p)
        
    if changed & (1<<vslot_types.VSLOT_SCALE): 
        vs.scale = readfloat(f)
    if changed & (1<<vslot_types.VLOT_ROTATION): 
        vs.rotation = readint(f)
    if changed & (1<<vslot_types.VSLOT_OFFSET):
        vs.xoffset = readint(f)
        vs.yoffset = readint(f)
    if changed & (1<<vslot_types.VSLOT_SCROLL):
        vs.scrollS = readfloat(f)
        vs.scrollT = readfloat(f)
    if changed & (1<<vslot_types.VSLOT_LAYER):
        vs.layer = readint(f)
    if changed & (1<<vslot_types.VSLOT_ALPHA):
        vs.alphafront = readfloat(f)
        vs.alphaback = readfloat(f)
    if changed & (1<<vslot_types.VSLOT_COLOR):
        vs.colorscale = vec(*struct.unpack("3f", f.read(12)))
    return vs