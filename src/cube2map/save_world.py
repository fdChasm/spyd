#@PydevCodeAnalysisIgnore
'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
import gzip
import struct
from cube2common.constants import MAPVERSION, cs_id_types, vslot_types,\
    octa_save_types, empty_material_types, layer_types
from cube2common.ivec import ivec, C, R
from cube2map.dimension import dimension
from cube2map.Cube import faceconvexity
from cube2map.visibletris import visibletris

def writeint(f, i):
    f.write(struct.pack('i', i))
    
def writeuint(f, i):
    f.write(struct.pack('I', i))
    
def writeushort(f, u):
    f.write(struct.pack('H', u))
    
def writechar(f, c):
    f.write(struct.pack('b', c))
    
def writefloat(f, v):
    f.write(struct.pack('f', v))

def save_map(map_filename, cube_map):
    nolms = True
    
    with gzip.open(map_filename, 'w') as f:
        f.write(struct.pack('4s', "OCTA"))
        writeint(f, MAPVERSION)
        writeint(f, 40)                                #header size
        writeint(f, cube_map.meta_data['wordsize'])    #world size
        writeint(f, 0)                                 #num ents
        writeint(f, 0)                                 #num pvs
        writeint(f, 0)                                 #light maps
        writeint(f, 0)                                 #blend map
        writeint(f, 1)                                 #num vars
        writeint(f, len(cube_map.vslots))              #num vslots
        
        writechar(f, cs_id_types.ID_SVAR)
        writeushort(f, len('skybox'))
        f.write('skybox')
        writeushort(f, len('skyboxes/remus/sky01'))
        f.write('skyboxes/remus/sky01')
        
        writechar(f, 3)
        f.write("fps\x00")
        
        # Extra data
        writeushort(f, 0)
        
        # texmru
        writeushort(f, 0)
        
        savevslots(f, cube_map.vslots)
        
        savec(f, cube_map, cube_map.octants, ivec(0, 0, 0), cube_map.meta_data['wordsize']>>1, nolms)
        
        #light maps would get saved here
        
def savevslot(f, vs, prev):
    writeint(f, vs.changed)
    writeint(f, prev)
    
    if vs.changed & (1<<vslot_types.VSLOT_SHPARAM):
        writeushort(f, len(vs.params))
        for p in vs.params:
            writeushort(f, len(p.name))
            f.write(p.name)
            for k in xrange(4):
                writeint(p.val[k])
    
    if vs.changed & (1<<vslot_types.VSLOT_SCALE):
        writefloat(f, vs.scale)
    if vs.changed & (1<<vslot_types.VSLOT_ROTATION):
        writeint(f, vs.rotation)
    if vs.changed & (1<<vslot_types.VSLOT_OFFSET):
        writeint(f, vs.xoffset)
        writeint(f, vs.yoffset)
    if vs.changed & (1<<vslot_types.VSLOT_SCROLL):
        writefloat(f, vs.scrollS)
        writefloat(f, vs.scrollT)
    if vs.changed & (1<<vslot_types.VSLOT_LAYER):
        writeint(f, vs.layer)
    if vs.changed & (1<<vslot_types.VSLOT_ALPHA):
        writefloat(f, vs.alphafront)
        writefloat(f, vs.alphaback)
    if vs.changed & (1<<vslot_types.VSLOT_COLOR):
        for k in xrange(3):
            writefloat(f, vs.colorscale[k])
        
def savevslots(f, vslots):
    numvslots = len(vslots)
    prev = [-1]*numvslots
    for i in xrange(numvslots):
        vs = vslots[i]
        if vs.changed: continue
        while 1:
            cur = vs
            while 1:
                vs = vs.next
                if vs is None or vs.index < numvslots: break
            if vs is None: break
            prev[vs.index] = cur.index
            
    lastroot = 0
    for i in xrange(numvslots):
        vs = vslots[i]
        if vs.changed == 0: continue
        if lastroot < i:
            writeuint(f, -(i - lastroot))
            savevslot(f, vs, prev[i])
            lastroot = i+1
    if lastroot < numvslots:
        writeuint(f, -(i - lastroot))

def savec(f, cube_map, c, o, size, nolms):
    
    for i in xrange(8):
        co = ivec(i, o.x, o.y, o.z, size)
        
        if len(c[i].children) > 0:
            writechar(f, octa_save_types.OCTSAV_CHILDREN)
            savec(f, cube_map, c[i].children, co, size>>1, nolms)
        else:
            oflags = 0
            surfmask = 0
            totalverts = 0
            if c[i].material != empty_material_types.MAT_AIR:
                oflags |= 0x40
                
            if not nolms:
                if c[i].merged:
                    oflags |= 0x80
                    
                if c[i].ext:
                    for j in xrange(6):
                        surf = c[i].ext.surfaces[j]
                        if not surf.used:
                            continue
                        
                        oflags |= 0x20
                        surfmask |= 1<<j
                        totalverts += surf.totalverts()

            if c[i].children:
                writechar(f, oflags | octa_save_types.OCTSAV_LODCUBE)
                
            elif c[i].isempty():
                writechar(f, oflags | octa_save_types.OCTSAV_EMPTY)
                
            elif c[i].isentirelysolid():
                writechar(f, oflags | octa_save_types.OCTSAV_SOLID)
                
            else:
                writechar(f, oflags | octa_save_types.OCTSAV_NORMAL)
                f.write(c[i].data)
    
            for j in xrange(6):
                writeushort(f, c[i].texture_walls[j])

            if oflags&0x40:
                writeushort(f, c[i].material);
                
            if oflags&0x80:
                writechar(f, c[i].merged)
                
            if oflags&0x20:
                writechar(f, surfmask)
                writechar(f, totalverts)
                
                for j in xrange(6):
                    if surfmask & (1<<j):
                        surf = c[i].ext.surfaces[j]
                        verts = c[i].ext.verts() + surf.verts;
                        
                        layerverts = surf.numverts & layer_types.MAXFACEVERTS
                        numverts = surf.totalverts()
                        
                        vertmask = 0
                        vertorder = 0
                        uvorder = 0
                        
                        dim = dimension(j)
                        vc = C[dim]
                        vr = R[dim]
                        
                        if numverts:
                            if c[i].merged & (1<<j):
                                vertmask |= 0x04;
                                if layerverts == 4:
                                    v = [verts[0].getxyz(), verts[1].getxyz(), verts[2].getxyz(), verts[3].getxyz()]
                                    for k in xrange(4):
                                        v0 = v[k]
                                        
                                        v1 = v[(k+1) & 3]
                                        v2 = v[(k+2) & 3]
                                        v3 = v[(k+3) & 3]
                                        
                                        if v1[vc] == v0[vc] and v1[vr] == v2[vr] and v3[vc] == v2[vc] and v3[vr] == v0[vr]:
                                            vertmask |= 0x01
                                            vertorder = k
                                            break
                            else:
                                vis = visibletris(c[i], cube_map, j, co.x, co.y, co.z, size)
                                if vis & 4 or faceconvexity(c[i], j) < 0:
                                    vertmask |= 0x01
                                if layerverts < 4 and vis & 2:
                                    vertmask |= 0x02
                                    
                            matchnorm = True
                            
                            for k in xrange(numverts): 
                                v = verts[k]
                                
                                if v.u or v.v:
                                    vertmask |= 0x40
                                     
                                if v.norm:
                                    vertmask |= 0x80
                                    if v.norm != verts[0].norm:
                                        matchnorm = False
                            
                            if matchnorm:
                                vertmask |= 0x08
                                
                            if vertmask & 0x40 and layerverts == 4:
                                for k in xrange(4):
                                    v0 = verts[k]
                                    
                                    v1 = verts[(k+1)&3]
                                    v2 = verts[(k+2)&3]
                                    v3 = verts[(k+3)&3]
                                    
                                    if v1.u == v0.u and v1.v == v2.v and v3.u == v2.u and v3.v == v0.v:
                                        if surf.numverts & layer_types.LAYER_DUP:
                                            b0 = verts[4+k]
                                            b1 = verts[4+((k+1)&3)]
                                            b2 = verts[4+((k+2)&3)]
                                            b3 = verts[4+((k+3)&3)]
                                            
                                            if b1.u != b0.u or b1.v != b2.v or b3.u != b2.u or b3.v != b0.v:
                                                continue
                                        
                                        uvorder = k
                                        vertmask |= 0x02 | (((k+4-vertorder)&3)<<4)
                                        break
                                    

                        surf.verts = vertmask
                        
                        f.write(surf, sizeof(surfaceinfo))
                        
                        hasxyz = (vertmask & 0x04)!=0
                        hasuv = (vertmask & 0x40)!=0
                        hasnorm = (vertmask & 0x80)!=0
                        
                        if layerverts == 4:
                        
                            if hasxyz and vertmask & 0x01:
                            
                                v0 = verts[vertorder].getxyz()
                                v2 = verts[(vertorder+2)&3].getxyz()
                                
                                writeushort(f, v0[vc])
                                writeushort(f, v0[vr])
                                writeushort(f, v2[vc])
                                writeushort(f, v2[vr])
                                
                                hasxyz = False
                            
                            if hasuv and vertmask & 0x02:
                            
                                v0 = verts[uvorder]
                                v2 = verts[(uvorder+2)&3]
                                
                                writeushort(f, v0.u)
                                writeushort(f, v0.v)
                                writeushort(f, v2.u)
                                writeushort(f, v2.v)
                                
                                if surf.numverts & layer_types.LAYER_DUP:
                                
                                    b0 = verts[4+uvorder]
                                    b2 = verts[4+((uvorder+2)&3)]
                                    
                                    writeushort(f, b0.u)
                                    writeushort(f, b0.v)
                                    writeushort(f, b2.u)
                                    writeushort(f, b2.v)
                                
                                hasuv = False;

                        if hasnorm and vertmask&0x08:
                            writeushort(f, verts[0].norm) 
                            hasnorm = False
                            
                        if hasxyz or hasuv or hasnorm:
                            for k in xrange(layerverts):
                                v = verts[(k+vertorder)%layerverts]
                                if hasxyz:
                                    xyz = v.getxyz()
                                    
                                    writeushort(f, xyz[vc])
                                    writeushort(f, xyz[vr])
                                
                                if hasuv:
                                    writeushort(f, v.u)
                                    writeushort(f, v.v)
                                    
                                if hasnorm:
                                    writeushort(f, v.norm)
                                    
                        if surf.numverts & layer_types.LAYER_DUP:
                            for k in xrange(layerverts):
                                v = verts[layerverts + (k+vertorder)%layerverts]
                                if hasuv:
                                    writeushort(f, v.u)
                                    writeushort(f, v.v)

            if c[i].children:
                savec(f, cube_map, c[i].children, co, size>>1, nolms)
