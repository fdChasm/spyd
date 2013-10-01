'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.threeplanesintersect import threeplaneintersect
import struct
from cube2map.Plane import Plane
from cube2common.constants import F_SOLID, empty_material_types,\
    hardcoded_textures, F_EMPTY
from cube2common.ivec import ivec
from cube2common.vec import vec
from cube2map.newcubeext import newcubeext
from cube2map.dimension import dimension, dimcoord

def edgeget(edge, coord):
    if coord:
        return edge >> 4
    else:
        return edge & 0xF

def edgeval(edge, coord, val):
    if coord:
        return ((edge) & 0xF) | ((val) << 4)
    else:
        return ((edge) & 0xF0) | (val)
    
def genvertp(c, p1, p2, p3, pl, solid):
    dim = 0;
    if p1.y==p2.y and p2.y==p3.y:
        dim = 1;
    elif p1.z==p2.z and p2.z==p3.z:
        dim = 2;

    coord = p1[dim];
    
    v1, v2, v3 = p1.copy(), p2.copy(), p3.copy()
    
    if solid:
        v1[dim] = coord*8
        v2[dim] = coord*8
        v3[dim] = coord*8
    else:
        v1[dim] = edgeval(c, p1, dim, coord)
        v2[dim] = edgeval(c, p2, dim, coord)
        v3[dim] = edgeval(c, p3, dim, coord)

    pl.toplane(v1.tovec(), v2.tovec(), v3.tovec());

def genedgespanvert(p, cube, v):
    p1 = ivec(8 - p.x, p.y, p.z);
    p2 = ivec(p.x, 8 - p.y, p.z);
    p3 = ivec(p.x, p.y, 8 - p.z);

    plane1 = Plane()
    plane2 = Plane()
    plane3 = Plane()

    genvertp(cube, p, p1, p2, plane1);
    genvertp(cube, p, p2, p3, plane2);
    genvertp(cube, p, p3, p1, plane3);

    if(plane1 == plane2): genvertp(cube, p, p1, p2, plane1, True)
    if(plane1 == plane3): genvertp(cube, p, p1, p2, plane1, True)
    if(plane2 == plane3): genvertp(cube, p, p2, p3, plane2, True)

    assert(threeplaneintersect(plane1, plane2, plane3, v));

    v.x = max(0.0, min(8.0, v.x))
    v.y = max(0.0, min(8.0, v.y))
    v.z = max(0.0, min(8.0, v.z))
    
def setsurfaces(c, surfs, verts, numverts):
    if c.ext is None or c.ext.maxverts < numverts:
        newcubeext(c, numverts, False)
    
    c.ext.surfaces = surfs
    c.ext.verts = verts
    
def flataxisface(c, orient):
    fx = c.faces[dimension(orient)]
    if dimcoord(orient):
        fx >>= 4
    return (fx & 0x0F0F0F0F) == 0x01010101*(fx & 0x0F)
    
def faceconvexity(*args):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        v = args[0]
        
        n = ivec()
        n.cross(ivec(v[1]).sub(v[0]), ivec(v[2]).sub(v[0]));
        return ivec(v[0]).sub(v[3]).dot(n);
        # 1 if convex, -1 if concave, 0 if flat
        
    elif len(args) == 2 and isinstance(args[0], Cube):
        c, orient = args
        
        if flataxisface(c, orient):
            return 0
        
        v = [None]*4
        genfaceverts(c, orient, v)
        return faceconvexity(v)
    
def touchingface(c, orient):
    face = c.faces[dimension(orient)];
    if dimcoord(orient):
        return (face & 0xF0F0F0F0) == 0x80808080
    else:
        return (face & 0x0F0F0F0F) == 0
    
def notouchingface(c, orient):
    face = c.faces[dimension(orient)];
    if dimcoord(orient):
        return (face&0x80808080)==0
    else:
        return ((0x88888888-face)&0x08080808) == 0

class CubeEdgeDataAccess(object):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

class CubeFaceDataAccess(object):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return struct.unpack_from('I', self.data, index * 4)[0]

    def __setitem__(self, index, value):
        struct.pack_into('I', self.data, index * 4, value)

class Cube(object):
    children = []
    ext = None
    data = bytearray(12)
    texture_walls = []
    material = 0
    merged = 0
    _vinfo = 0

    def __init__(self, face=F_EMPTY, mat=empty_material_types.MAT_AIR):
        self.data = bytearray(12)
        self.edges = CubeEdgeDataAccess(self.data)
        self.faces = CubeFaceDataAccess(self.data)
        self.texture_walls = [hardcoded_textures.DEFAULT_GEOM] * 6
        self.material = mat
        self.setfaces(face)

    @property
    def escaped(self):
        return self._vinfo

    @escaped.setter
    def escaped(self, value):
        self._vinfo = value

    @property
    def visible(self):
        return self._vinfo

    @visible.setter
    def visible(self, value):
        self._vinfo = value

    def setfaces(self, value):
        self.faces[0] = value
        self.faces[1] = value
        self.faces[2] = value

    def isentirelysolid(self):
        return self.faces[0] == F_SOLID and self.faces[1] == F_SOLID and self.faces[2] == F_SOLID

    def isempty(self):
        return self.faces[0] == F_EMPTY

    def copy(self):
        c = Cube()
        c.children = self.children
        c.ext = self.ext
        c.data = bytearray(self.data)
        c.edges = CubeEdgeDataAccess(self.data)
        c.faces = CubeFaceDataAccess(self.data)
        c.texture_walls = self.texture_walls
        c.merged = self.merged
        c._vinfo = self._vinfo

    def setcubeedge(self, d, x, y, v):
        self.edges[(((d) << 2) + ((y) << 1) + (x))] = v

    def getcubeedge(self, d, x, y):
        return self.edges[(((d) << 2) + ((y) << 1) + (x))]

    def edgespan2vectorcube(self):
        if self.isentirelysolid() or self.isempty(): return
        for x in xrange(2):
            for y in xrange(2):
                for z in xrange(2):
                    p = ivec(8 * x, 8 * y, 8 * z)
                    v = vec(0, 0, 0)

                    o = self.copy()

                    genedgespanvert(p, o, v)

                    self.setcubeedge(0, y, z, edgeval(self.getcubeedge(0, y, z), x, int(v.x + 0.49)))
                    self.setcubeedge(1, z, x, edgeval(self.getcubeedge(1, z, x), y, int(v.y + 0.49)))
                    self.setcubeedge(2, x, y, edgeval(self.getcubeedge(2, x, y), z, int(v.z + 0.49)))

def newcubes(face=F_EMPTY, mat=empty_material_types.MAT_AIR):
    return map(lambda _: Cube(face, mat), xrange(8))

def genfaceverts(c, orient, v):
    if orient == 0:
            v[0] = ivec(edgeget(c.getcubeedge(0, 1, 1), 0), edgeget(c.getcubeedge(1, 1, 0), 1), edgeget(c.getcubeedge(2, 0, 1), 1));
            v[1] = ivec(edgeget(c.getcubeedge(0, 1, 0), 0), edgeget(c.getcubeedge(1, 0, 0), 1), edgeget(c.getcubeedge(2, 0, 1), 0));
            v[2] = ivec(edgeget(c.getcubeedge(0, 0, 0), 0), edgeget(c.getcubeedge(1, 0, 0), 0), edgeget(c.getcubeedge(2, 0, 0), 0));
            v[3] = ivec(edgeget(c.getcubeedge(0, 0, 1), 0), edgeget(c.getcubeedge(1, 1, 0), 0), edgeget(c.getcubeedge(2, 0, 0), 1));
    elif orient == 1:
            v[0] = ivec(edgeget(c.getcubeedge(0, 1, 1), 1), edgeget(c.getcubeedge(1, 1, 1), 1), edgeget(c.getcubeedge(2, 1, 1), 1));
            v[1] = ivec(edgeget(c.getcubeedge(0, 0, 1), 1), edgeget(c.getcubeedge(1, 1, 1), 0), edgeget(c.getcubeedge(2, 1, 0), 1));
            v[2] = ivec(edgeget(c.getcubeedge(0, 0, 0), 1), edgeget(c.getcubeedge(1, 0, 1), 0), edgeget(c.getcubeedge(2, 1, 0), 0));
            v[3] = ivec(edgeget(c.getcubeedge(0, 1, 0), 1), edgeget(c.getcubeedge(1, 0, 1), 1), edgeget(c.getcubeedge(2, 1, 1), 0));
    elif orient == 2:
            v[0] = ivec(edgeget(c.getcubeedge(0, 0, 1), 1), edgeget(c.getcubeedge(1, 1, 1), 0), edgeget(c.getcubeedge(2, 1, 0), 1));
            v[1] = ivec(edgeget(c.getcubeedge(0, 0, 1), 0), edgeget(c.getcubeedge(1, 1, 0), 0), edgeget(c.getcubeedge(2, 0, 0), 1));
            v[2] = ivec(edgeget(c.getcubeedge(0, 0, 0), 0), edgeget(c.getcubeedge(1, 0, 0), 0), edgeget(c.getcubeedge(2, 0, 0), 0));
            v[3] = ivec(edgeget(c.getcubeedge(0, 0, 0), 1), edgeget(c.getcubeedge(1, 0, 1), 0), edgeget(c.getcubeedge(2, 1, 0), 0));
    elif orient == 3:
            v[0] = ivec(edgeget(c.getcubeedge(0, 1, 0), 0), edgeget(c.getcubeedge(1, 0, 0), 1), edgeget(c.getcubeedge(2, 0, 1), 0));
            v[1] = ivec(edgeget(c.getcubeedge(0, 1, 1), 0), edgeget(c.getcubeedge(1, 1, 0), 1), edgeget(c.getcubeedge(2, 0, 1), 1));
            v[2] = ivec(edgeget(c.getcubeedge(0, 1, 1), 1), edgeget(c.getcubeedge(1, 1, 1), 1), edgeget(c.getcubeedge(2, 1, 1), 1));
            v[3] = ivec(edgeget(c.getcubeedge(0, 1, 0), 1), edgeget(c.getcubeedge(1, 0, 1), 1), edgeget(c.getcubeedge(2, 1, 1), 0));
    elif orient == 4:
            v[0] = ivec(edgeget(c.getcubeedge(0, 0, 0), 0), edgeget(c.getcubeedge(1, 0, 0), 0), edgeget(c.getcubeedge(2, 0, 0), 0));
            v[1] = ivec(edgeget(c.getcubeedge(0, 1, 0), 0), edgeget(c.getcubeedge(1, 0, 0), 1), edgeget(c.getcubeedge(2, 0, 1), 0));
            v[2] = ivec(edgeget(c.getcubeedge(0, 1, 0), 1), edgeget(c.getcubeedge(1, 0, 1), 1), edgeget(c.getcubeedge(2, 1, 1), 0));
            v[3] = ivec(edgeget(c.getcubeedge(0, 0, 0), 1), edgeget(c.getcubeedge(1, 0, 1), 0), edgeget(c.getcubeedge(2, 1, 0), 0));
    elif orient == 5:
            v[0] = ivec(edgeget(c.getcubeedge(0, 0, 1), 0), edgeget(c.getcubeedge(1, 1, 0), 0), edgeget(c.getcubeedge(2, 0, 0), 1));
            v[1] = ivec(edgeget(c.getcubeedge(0, 0, 1), 1), edgeget(c.getcubeedge(1, 1, 1), 0), edgeget(c.getcubeedge(2, 1, 0), 1));
            v[2] = ivec(edgeget(c.getcubeedge(0, 1, 1), 1), edgeget(c.getcubeedge(1, 1, 1), 1), edgeget(c.getcubeedge(2, 1, 1), 1));
            v[3] = ivec(edgeget(c.getcubeedge(0, 1, 1), 0), edgeget(c.getcubeedge(1, 1, 0), 1), edgeget(c.getcubeedge(2, 0, 1), 1));
