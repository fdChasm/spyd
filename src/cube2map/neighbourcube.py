#@PydevCodeAnalysisIgnore
'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.ivec import ivec
from cube2map.dimension import dimension, dimcoord, octastep

def neighbourcube(c, cube_map, orient, x, y, z, size, ro, rsize):
    worldsize = cube_map.meta_data['wordsize']
    
    n = ivec(x, y, z)
    dim = dimension(orient);
    diff = n[dim];
    
    if dimcoord(orient):
        n[dim] += size
    else:
        n[dim] -= size
        
    diff ^= n[dim];
    
    if diff >= uint(worldsize):
        ro = n
        rsize = size
        return c
        
    scale = worldscale
    
    nc = cube_map.octants
    
    if neighbourdepth >= 0:
        scale -= neighbourdepth + 1
        diff >>= scale
        
        while 1:
            scale += 1
            dif >>= 1
            if diff == 0:
                break
        
        nc = neighbourstack[worldscale - scale]
    
    scale -= 1
    
    nc = nc[octastep(n.x, n.y, n.z, scale)]
    if (size>>scale == 0) and nc.children is not None:
        while 1:
            scale -= 1
            nc = nc[0].children[octastep(n.x, n.y, n.z, scale)]
            
            if (size>>scale == 0) and nc.children is not None:
                break
        
    ro = n.mask(~0<<scale)
    rsize = 1<<scale
    return nc[0]
