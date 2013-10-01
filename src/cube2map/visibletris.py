#@PydevCodeAnalysisIgnore
'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.ivec import ivec
from cube2map.Cube import genfaceverts, notouchingface, touchingface
from cube2map.dimension import opposite, dimension, dimcoord
from cube2common.constants import empty_material_types, F_SOLID
from cube2map.insideface import insideface
from cube2map.facevec import facevec
from cube2map.occludesface import occludesface
from cube2map.genfacevecs import genfacevecs
from cube2map.faceedges import faceedges
from cube2map.neighbourcube import neighbourcube

# more expensive version that checks both triangles of a face independently
def visibletris(c, cube_map, orient, x, y, z, size, nmat, matmask):

    vis = 3
    touching = 0xF
    
    e1, e2, e3, n = [ivec() for _ in xrange(4)]
    
    
    v = [None]*4
    genfaceverts(c, orient, v)
    
    e1 = v[1]
    e2 = v[2]
    e3 = v[0]
    
    n.cross((e1).sub(v[0]), (e2).sub(v[0]))
    convex = (e3).sub(v[3]).dot(n)
    if convex == 0:
    
        if ivec().cross(e3, e2).iszero():
            if n.iszero():
                return 0
            vis = 1
            touching = 0xF & ~(1<<3)
            
        elif n.iszero():
            vis = 2
            touching = 0xF&~(1<<1)
    

    dim = dimension(orient)
    coord = dimcoord(orient)
    
    if v[0][dim] != coord*8: touching &= ~(1<<0)
    if v[1][dim] != coord*8: touching &= ~(1<<1)
    if v[2][dim] != coord*8: touching &= ~(1<<2)
    if v[3][dim] != coord*8: touching &= ~(1<<3)
    
    # mask of triangles not touching
    notouchmasks = [
      # order 0: flat or convex
       # 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
        [ 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 3, 0 ],
      # order 1: concave
        [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 0 ],
    ]
    order = 1 if convex < 0 else 0
    notouch = notouchmasks[order][touching]
    
    if (vis&notouch)==vis:
        return vis

    no = ivec()
    nsize = 0
    
    o = neighbourcube(c, cube_map, orient, x, y, z, size, no, nsize)
    
    if o is c:
        return 0
    
    if c.material & matmask == nmat:
        nmat = empty_material_types.MAT_AIR

    vo = ivec(x, y, z)
    
    vo.mask(0xFFF)
    no.mask(0xFFF)
    
    cf = [facevec() for _ in xrange(4)]
    of = [facevec() for _ in xrange(4)]
    
    opp = opposite(orient)
    numo = 0
    numc = 0
    
    if nsize > size or (nsize == size and o.children == 0):
    
        if o.isempty() or notouchingface(o, opp):
            return vis
        
        if nmat != empty_material_types.MAT_AIR and (o.material & matmask) == nmat:
            return vis
       
        if o.isentirelysolid() or (touchingface(o, opp) and faceedges(o, opp) == F_SOLID):
            return vis & notouch

        numc = genfacevecs(c, orient, vo, size, False, cf, v)
        numo = genfacevecs(o, opp, no, nsize, False, of)
        
        if numo < 3:
            return vis
        
        if insideface(cf, numc, of, numo):
            return vis & notouch
    
    else:
        numc = genfacevecs(c, orient, vo, size, False, cf, v)
        if occludesface(o, opp, no, nsize, vo, size, empty_material_types.MAT_AIR, nmat, matmask, cf, numc):
            return vis & notouch
    
    if vis != 3 or notouch:
        return vis

    triverts = [
      # order
        [ # coord
            [ [ 1, 2, 3 ], [ 0, 1, 3 ] ], # verts
            [ [ 0, 1, 2 ], [ 0, 2, 3 ] ]
        ],
        [ # coord
            [ [ 0, 1, 2 ], [ 3, 0, 2 ] ], # verts
            [ [ 1, 2, 3 ], [ 1, 3, 0 ] ]
        ]
    ]

    while 1:
        for i in xrange(2):
            verts = triverts[order][coord][i]
            
            tf = [cf[verts[0]], cf[verts[1]], cf[verts[2]]]
            
            if numo > 0:
                if insideface(tf, 3, of, numo) == 0:
                    continue
                
            elif occludesface(o, opp, no, nsize, vo, size, empty_material_types.MAT_AIR, nmat, matmask, tf, 3) == 0:
                continue
            
            return vis & ~(1<<i)
        
        vis |= 4;
        
        order += 1
        if order <= 1: break

    return 3;
