#@PydevCodeAnalysisIgnore
'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
import zlib
import gzip
import struct
from cube2map.utils import readint, readchar, clamp, floor, ushort, readuchar,\
    readbvec, readushort
from cube2map.encodenormal import encodenormal
from cube2map.newcubeext import newcubeext
from cube2map.SurfaceInfo import SurfaceInfo
from cube2map.VertInfo import VertInfo
from cube2map.Cube import Cube, setsurfaces, genfaceverts, newcubes
from cube2map.facecoords import facecoords
from cube2common.constants import layer_types, lighting_types, LM_PACKW,\
    USHRT_MAX, LM_PACKH, octa_save_types, F_SOLID, F_EMPTY, empty_material_types,\
    cs_id_types, MAXENTS
from cube2common.ivec import ivec, C, R
from cube2common.bvec import bvec
from cube2map.errors import OctaError
from cube2map.convertoldmaterial import convertoldmaterial
from cube2map.SurfaceCompat import SurfaceCompat
from cube2map.NormalsCompat import NormalsCompat
from cube2map.MergesCompat import MergesCompat
from cube2common.vec import vec
from cube2map.load_vslots import load_vslots
from cube2map.CubeMap import CubeMap

def convertoldsurfaces(c, co, size, srcsurfs, hassurfs, normals, hasnorms, merges, hasmerges):
    dstsurfs = map(lambda _: SurfaceInfo(), xrange(6))
    verts = map(lambda _: VertInfo(), xrange(6*2*layer_types.MAXFACEVERTS))
    
    totalverts = 0
    numsurfs = 6
    
    for i in xrange(6):
        if (hassurfs|hasnorms|hasmerges)&(1<<i):
            dst = dstsurfs[i]
            curverts = None
            numverts = 0
            
            src = None
            blend = None
            
            if hassurfs & (1<<i):
            
                src = srcsurfs[i]
                
                if src.layer & 2:
                
                    blend = srcsurfs[numsurfs]
                    numsurfs += 1
                    
                    dst.lmid[0] = src.lmid;
                    dst.lmid[1] = blend.lmid;
                    dst.numverts |= layer_types.LAYER_BLEND;
                    
                    if blend.lmid >= lighting_types.LMID_RESERVED:
                        if src.x != blend.x or src.y != blend.y or src.w != blend.w or src.h != blend.h or (not src.compare_textcoords(blend)):
                            dst.numverts |= layer_types.LAYER_DUP
                
                elif src.layer == 1:
                    dst.lmid[1] = src.lmid
                    dst.numverts |= layer_types.LAYER_BOTTOM
                else:
                    dst.lmid[0] = src.lmid
                    dst.numverts |= layer_types.LAYER_TOP
            
            else:
                dst.numverts |= layer_types.LAYER_TOP
            
            uselms = hassurfs & (1<<i) and (dst.lmid[0] >= lighting_types.LMID_RESERVED or dst.lmid[1] >= lighting_types.LMID_RESERVED or dst.numverts & ~layer_types.LAYER_TOP)
            usemerges = hasmerges&(1<<i) and merges[i].u1 < merges[i].u2 and merges[i].v1 < merges[i].v2
            usenorms = hasnorms & (1<<i) and normals[i].normals[0] != bvec(128, 128, 128)
            
            if uselms or usemerges or usenorms:
            
                v = map(lambda _: ivec(), xrange(4))
                pos = map(lambda _: ivec(), xrange(4))
                
                e1 = ivec()
                e2 = ivec()
                e3 = ivec()
                
                n = ivec()
                
                vo  = ivec(co).mask(0xFFF).shl(3)
                
                genfaceverts(c, i, v); 
                
                e1 = v[1]
                e2 = v[2]
                
                n.cross((e1).sub(v[0]), (e2).sub(v[0]));
                if usemerges:
                
                    m = merges[i]
                    offset = -n.dot(v[0].mul(size).add(vo)),
                    dim = dimension(i)
                    vc = C[dim]
                    vr = R[dim]
                    
                    for k in xrange(4):
                    
                        coords = facecoords[i][k]
                        if coords[vc]:
                            cc = m.u2
                        else:
                            cc = m.u1
                            
                        if coords[vr]:
                            rc = m.v2
                        else:
                            rc = m.v1
                        
                        dc = -(offset + n[vc]*cc + n[vr]*rc)/n[dim]
                        
                        mv = pos[k]
                        
                        mv[vc] = cc
                        mv[vr] = rc
                        mv[dim] = dc

                else:
                    e3 = v[0]
                    convex = (e3).sub(v[3]).dot(n)
                    vis = 3;
                    if convex == 0:
                    
                        if ivec(0, 0, 0).cross(e3, e2).iszero():
                            if not n.iszero():
                                vis = 1 
                        elif n.iszero():
                            vis = 2
                    
                    if convex < 0:
                        order = 1
                    else:
                        order = 0
                    
                    pos[0] = v[order].mul(size).add(vo);
                    
                    if vis & 1:
                        pos[1] = v[order+1].mul(size).add(vo)
                    else:
                        pos[1] = pos[0]
                        
                    pos[2] = v[order+2].mul(size).add(vo);
                    
                    if vis & 2:
                        pos[3] = v[(order+3)&3].mul(size).add(vo)
                    else:
                        pos[3] = pos[0];
                
                curverts = verts + totalverts;
                
                for k in xrange(4):
                    if k > 0 and (pos[k] == pos[0] or pos[k] == pos[k-1]): continue
                    dv = curverts[numverts]
                    numverts += 1
                    dv.setxyz(pos[k])
                    
                    if uselms:
                        u = src.x + (src.texcoords[k*2] / 255.0) * (src.w - 1)
                        v = src.y + (src.texcoords[k*2+1] / 255.0) * (src.h - 1)
                        
                        dv.u = ushort(floor(clamp((u) * float(USHRT_MAX+1)/LM_PACKW + 0.5, 0.0, float(USHRT_MAX))))
                        dv.v = ushort(floor(clamp((v) * float(USHRT_MAX+1)/LM_PACKH + 0.5, 0.0, float(USHRT_MAX))))
                    
                    else:
                        dv.u = 0
                        dv.v = 0
                        
                    if usenorms and normals[i].normals[k] != bvec(128, 128, 128):
                        dv.norm = encodenormal(normals[i].normals[k].tovec().normalize())
                    else:
                        dv.norm = 0
                
                dst.verts = totalverts;
                dst.numverts |= numverts;
                totalverts += numverts;
                if dst.numverts & layer_types.LAYER_DUP:
                    for k in xrange(4):
                        if k > 0 and (pos[k] == pos[0] or pos[k] == pos[k-1]): continue
                        bv = verts[totalverts]
                        totalverts += 1
                        bv.setxyz(pos[k])
                        
                        bv.u = ushort(floor(clamp((blend.x + (blend.texcoords[k*2] / 255.0) * (blend.w - 1)) * float(USHRT_MAX+1)/LM_PACKW, 0.0, float(USHRT_MAX))))
                        bv.v = ushort(floor(clamp((blend.y + (blend.texcoords[k*2+1] / 255.0) * (blend.h - 1)) * float(USHRT_MAX+1)/LM_PACKH, 0.0, float(USHRT_MAX))))
                        
                        if usenorms and normals[i].normals[k] != bvec(128, 128, 128):
                            bv.norm = encodenormal(normals[i].normals[k].tovec().normalize())
                        else:
                            bv.norm = 0

    setsurfaces(c, dstsurfs, verts, totalverts)

def loadc(version, f, cube, co, size):
    haschildren = False
    
    octsav = readchar(f)
    
    val = octsav & 0x7
    if val == octa_save_types.OCTSAV_CHILDREN:
        cube.children = loadchildren(version, f, co, size>>1)
        return
    elif val == octa_save_types.OCTSAV_LODCUBE:
        haschildren = True
    elif val == octa_save_types.OCTSAV_EMPTY:
        cube.setfaces(F_EMPTY)
    elif val == octa_save_types.OCTSAV_SOLID:
        cube.setfaces(F_SOLID)
    elif val == octa_save_types.OCTSAV_NORMAL:
        cube.data = bytearray(f.read(12))
    else:
        raise OctaError()
    
    if version < 14:
        cube.texture = struct.unpack("6b", f.read(6))
    else:
        cube.texture = struct.unpack("6H", f.read(12))
        
    if version < 7:
        f.read(3)
    elif version <= 31:
        mask = readchar(f)
        if mask & 0x80:
            mat = readchar(f)
            if version < 27:
                matconv = [empty_material_types.MAT_AIR, empty_material_types.MAT_WATER, empty_material_types.MAT_CLIP, empty_material_types.MAT_GLASS|empty_material_types.MAT_CLIP, empty_material_types.MAT_NOCLIP, empty_material_types.MAT_LAVA|empty_material_types.MAT_DEATH, empty_material_types.MAT_GAMECLIP, empty_material_types.MAT_DEATH]
                cube.material = matconv[mat] if mat < len(matconv) else empty_material_types.MAT_AIR
            else:
                cube.material = convertoldmaterial(mat)
                
        surfaces = map(lambda _: SurfaceCompat(), xrange(12))
        normals = map(lambda _: NormalsCompat(), xrange(6))
        merges = map(lambda _: MergesCompat(), xrange(6))
        
        hassurfs = 0
        hasnorms = 0
        hasmerges = 0
        
        if mask & 0x3F:
            numsurfs = 6
            i = 0
            while i < numsurfs:
                if i >= 6 or mask & (1 << i):
                    surfaces[i] = SurfaceCompat.read(f)
                    if version < 10:
                        surfaces[i].lmid += 1
                    if version < 18:
                        if surfaces[i].lmid >= lighting_types.LMID_AMBIENT1: surfaces[i].lmid += 1
                        if surfaces[i].lmid >= lighting_types.LMID_BRIGHT1: surfaces[i].lmid += 1
                    if version < 19:
                        if surfaces[i].lmid >= lighting_types.LMID_DARK: surfaces[i].lmid += 2
                    if i < 6:
                        if mask & 0x40:
                            hasnorms |= 1<<i
                            normals[i] = NormalsCompat.read(f)
                        if surfaces[i].layer != 0 or surfaces[i] != lighting_types.LMID_AMBIENT:
                            hassurfs |= 1<<i
                        if surfaces[i].layer & 2:
                            numsurfs += 1
                
        if version <= 8:
            cube.edgespan2vectorcube()
            
        if version <= 11:
            cube.faces[0], cube.faces[2] = cube.faces[2], cube.faces[0]
            cube.texture[0], cube.texture[4] = cube.texture[4], cube.texture[0]
            cube.texture[1], cube.texture[5] = cube.texture[5], cube.texture[1]
            if hassurfs & 0x33:
                cube.surfaces[0], cube.surfaces[4] = cube.surfaces[4], cube.surfaces[0]
                cube.surfaces[1], cube.surfaces[5] = cube.surfaces[5], cube.surfaces[1]
                hassurfs = (hassurfs&~0x33) | ((hassurfs&0x30)>>4) | ((hassurfs&0x03)<<4)
                
        if version >= 20:
            if octsav&0x80:
                merged = readchar(f)
                cube.merged = merged&0x3F
                if merged&0x80:
                    mask = readchar(f)
                    if mask:
                        hasmerges = mask&0x3F
                        
                        for i in xrange(6):
                            if mask&(1<<i):
                                merges[i] = MergesCompat.read(f)
                                m = merges[i]
                                if version <= 25:
                                    uorigin = m.u1 & 0xE000
                                    vorigin = m.v1 & 0xE000
                                    m.u1 = (m.u1 - uorigin) << 2
                                    m.u2 = (m.u2 - uorigin) << 2
                                    m.v1 = (m.v1 - vorigin) << 2
                                    m.v2 = (m.v2 - vorigin) << 2
                                    
        if hassurfs or hasnorms or hasmerges:
            convertoldsurfaces(cube, co, size, surfaces, hassurfs, normals, hasnorms, merges, hasmerges)
    else:
        if octsav&0x40:
            if version <= 32:
                mat = readchar(f)
                cube.material = convertoldmaterial(mat)
            else:
                cube.material = readuchar(f)
        
        if octsav & 0x80:
            cube.merged = readchar(f)

        if octsav & 0x20:
            surfmask = readchar(f)
            totalverts = readchar(f)
            
            newcubeext(cube, totalverts, False)
            
            cube.ext.surfaces = map(lambda _: SurfaceInfo(), xrange(6))
            cube.ext.verts = map(lambda _: VertInfo(), xrange(cube.ext.maxverts))
            
            offset = 0
            
            for i in xrange(6):
                if surfmask & (1<<i):
                    cube.ext.surfaces[i] = SurfaceInfo.read(f)
                    surf = cube.ext.surfaces[i]
                    
                    vertmask = surf.verts 
                    numverts = surf.totalverts;
                    
                    if numverts == 0:
                        surf.verts = 0
                        continue
                    
                    surf.verts = offset
                    
                    verts = cube.ext.verts
                    
                    verts = cube.ext.verts[offset/12:]
                    offset += numverts
                    
                    v = map(lambda _: ivec(), xrange(4))
                    n = 0
                    
                    layerverts = surf.numverts & layer_types.MAXFACEVERTS
                    dim = dimension(i)
                    vc = C[dim]
                    vr = R[dim]
                    bias = 0
                    
                    genfaceverts(cube, i, v)
                    
                    hasxyz = (vertmask&0x04)!=0
                    hasuv = (vertmask&0x40)!=0
                    hasnorm = (vertmask&0x80)!=0
                    
                    if hasxyz:
                        e1, e2, e3 = ivec(), ivec(), ivec()
                        
                        e1 = v[1]
                        e2 = v[2]
                        n.cross((e1).sub(v[0]), (e2).sub(v[0]))
                        
                        if n.iszero():
                            e3 = v[3]
                            n.cross(e2, (e3).sub(v[0]))
                        
                        bias = -n.dot(ivec(v[0]).mul(size).add(ivec(co).mask(0xFFF).shl(3)));
                    else:
                        if layerverts < 4:
                            vis = 2 if vertmask&0x02 else 1
                        else:
                            vis = 3
                        
                        if vertmask&0x01:
                            order = 1
                        else:
                            order = 0
                        
                        k = 0
                        
                        vo = ivec(co).mask(0xFFF).shl(3)
                        
                        verts[k].setxyz(v[order].mul(size).add(vo))
                        k += 1
                        
                        if vis & 1:
                            verts[k].setxyz(v[order+1].mul(size).add(vo))
                            k += 1
                        
                        verts[k].setxyz(v[order+2].mul(size).add(vo));
                        k += 1
                        
                        if vis & 2:
                            verts[k].setxyz(v[(order+3)&3].mul(size).add(vo))
                            k += 1

                    if layerverts == 4:
                        if hasxyz and vertmask & 0x01:
                            c1, r1, c2, r2 = struct.unpack("4H", f.read(8))
                            
                            xyz = ivec()
                            
                            xyz[vc] = c1; xyz[vr] = r1
                            xyz[dim] = -(bias + n[vc]*xyz[vc] + n[vr]*xyz[vr])/n[dim]
                            verts[0].setxyz(xyz)
                            
                            xyz[vc] = c1; xyz[vr] = r2
                            xyz[dim] = -(bias + n[vc]*xyz[vc] + n[vr]*xyz[vr])/n[dim]
                            verts[1].setxyz(xyz)
                            
                            xyz[vc] = c2; xyz[vr] = r2
                            xyz[dim] = -(bias + n[vc]*xyz[vc] + n[vr]*xyz[vr])/n[dim]
                            verts[2].setxyz(xyz)
                            
                            xyz[vc] = c2; xyz[vr] = r1
                            xyz[dim] = -(bias + n[vc]*xyz[vc] + n[vr]*xyz[vr])/n[dim]
                            verts[3].setxyz(xyz)
                            
                            hasxyz = False;
                        
                        if hasuv and vertmask & 0x02:
                            uvorder = (vertmask & 0x30)>>4
                            
                            v0 = verts[uvorder]
                            v1 = verts[(uvorder+1)&3]
                            v2 = verts[(uvorder+2)&3]
                            v3 = verts[(uvorder+3)&3]
                            
                            v0.u, v0.v = struct.unpack("2H", f.read(4))
                            v2.u, v2.v = struct.unpack("2H", f.read(4))
                            
                            v1.u = v0.u
                            v1.v = v2.v
                            
                            v3.u = v2.u
                            v3.v = v0.v
                            
                            if surf.numverts & layer_types.LAYER_DUP:
                            
                                b0 = verts[4+uvorder]
                                b1 = verts[4+((uvorder+1)&3)]
                                b2 = verts[4+((uvorder+2)&3)]
                                b3 = verts[4+((uvorder+3)&3)]
                                
                                b0.u, b0.v = struct.unpack("2H", f.read(4))
                                b2.u, b2.v = struct.unpack("2H", f.read(4))
                                
                                b1.u = b0.u; b1.v = b2.v;
                                b3.u = b2.u; b3.v = b0.v;
                            
                            hasuv = False
                    
                    if hasnorm and vertmask & 0x08:
                    
                        norm = readushort(f)
                        for k in xrange(layerverts):
                            verts[k].norm = norm
                        hasnorm = False
                    
                    if hasxyz or hasuv or hasnorm:
                        for k in xrange(layerverts):
                            v = verts[k]
                            if hasxyz:
                            
                                xyz = ivec()
                                xyz[vc], xyz[vr] = struct.unpack("2H", f.read(4))
                                
                                xyz[dim] = -(bias + n[vc]*xyz[vc] + n[vr]*xyz[vr])/n[dim];
                                v.setxyz(xyz);
                            
                            if hasuv:
                                v.u, v.v = struct.unpack("2H", f.read(4))
                                
                            if hasnorm:
                                v.norm = readushort(f)
                    
                    if surf.numverts & layer_types.LAYER_DUP:
                        for k in xrange(layerverts):
                            v = verts[k+layerverts]
                            t = verts[k]
                            
                            v.setxyz(t.x, t.y, t.z)
                            
                            if hasuv:
                                v.u, v.v = struct.unpack("2H", f.read(4))

                            v.norm = t.norm
    
    if haschildren:
        cube.children = loadchildren(version, f, co, size>>1)
    else:
        cube.children = None
    
    return cube

def loadchildren(version, f, co, size):
    cubes = newcubes()
    for i in xrange(len(cubes)):
        loadc(version, f, cubes[i], ivec(i, co.x, co.y, co.z, size), size)
    return cubes

def read_map_data(map_filename):
    meta_data = {'vars': {}, 'ents': []}
    
    with gzip.open(map_filename) as f:
        magic, version, headersize, worldsize, numents, numpvs, lightmaps = struct.unpack("4s6i", f.read(28))
        
        meta_data['version'] = version
        meta_data['headersize'] = headersize
        meta_data['worldsize'] = worldsize
        meta_data['numents'] = numents
        meta_data['numpvs'] = numpvs
        meta_data['lightmaps'] = lightmaps
        
        if version <= 28:
            lightprecision, lighterror, lightlod = struct.unpack("3i", f.read(12))
            
            ambient         = struct.unpack("B",   f.read(1))
            watercolor      = struct.unpack("3B",  f.read(3))
            blendmap        = struct.unpack("B",   f.read(1))
            lerpangle       = struct.unpack("B",   f.read(1))
            lerpsubdiv      = struct.unpack("B",   f.read(1))
            lerpsubdivsize  = struct.unpack("B",   f.read(1))
            bumperror       = struct.unpack("B",   f.read(1))
            skylight        = struct.unpack("3B",  f.read(3))
            lavacolor       = struct.unpack("3B",  f.read(3))
            waterfallcolor  = struct.unpack("3B",  f.read(3))
            reserved        = struct.unpack("10B", f.read(10))
            
            maptitle = struct.unpack("128s", f.read(128))
            
            meta_data['vars']['maptitle'] = maptitle
        else:
            if version <= 29:
                blendmap, numvars = struct.unpack("2i", f.read(8))
            else:
                blendmap, numvars, numvslots = struct.unpack("3i", f.read(12))
           
        if version <= 28:
            numvars = 0
    
        if version <= 29:
            numvslots = 0
                
        meta_data['blendmap'] = blendmap
        meta_data['numvars'] = numvars
        meta_data['numvslots'] = numvslots
    
        for i in xrange(numvars):
            var_type = struct.unpack("b", f.read(1))[0]
            ilen     = struct.unpack("<H", f.read(2))[0]
            var_name = f.read(ilen)
            if var_type == cs_id_types.ID_VAR:
                var_value = struct.unpack("i", f.read(4))[0]
            elif var_type == cs_id_types.ID_FVAR:
                var_value = struct.unpack("f", f.read(4))[0]
            elif var_type == cs_id_types.ID_SVAR:
                slen = struct.unpack("H", f.read(2))[0]
                var_value = f.read(slen)
                
            #print "{:.8}: {:.32s} = {}".format(cs_id_types.by_value(var_type), var_name, var_value)
            
            meta_data['vars'][var_name] = var_value
            
        if version >= 16:
            gt_len = struct.unpack("b", f.read(1))[0]
            game_type = f.read(gt_len+1)
        else:
            game_type = 'fps'
            
        meta_data['gametype'] = game_type

        if version >= 16:
            eif = struct.unpack("H", f.read(2))[0]
            extra_size = struct.unpack("H", f.read(2))[0]
            edata = f.read(extra_size)
            
        print eif, extra_size, edata
    
        if version < 14:
            f.read(256)
        else:
            nummru = struct.unpack("H", f.read(2))[0]
            f.read(nummru*2)
            
        for i in range(min(numents, MAXENTS)):
            x, y, z = struct.unpack("3f", f.read(12))
            attrs = struct.unpack('5h', f.read(10))
            ent_type, reserved = struct.unpack('2B', f.read(2))
                
            ent = {'id': i, 'type': ent_type, 'x': x, 'y': y, 'z': z, 'attrs': attrs, 'reserved': reserved}
            meta_data['ents'].append(ent)
            
        vslots = load_vslots(f, numvslots)
        worldroot = loadchildren(version, f, vec(0, 0, 0), worldsize>>1)
    
    try:
        with gzip.open(map_filename) as f:
            meta_data['crc'] = zlib.crc32(f.read()) & 0xffffffff
    except IOError:
        meta_data['crc'] = 0

    cube_map = CubeMap()
    cube_map.vslots = vslots
    cube_map.octants = worldroot
    cube_map.meta_data = meta_data
        
    return cube_map