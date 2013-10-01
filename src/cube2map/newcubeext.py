'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.growcubeext import growcubeext
from cube2map.SurfaceInfo import SurfaceInfo

def newcubeext(cube, maxverts=0, init=True):
    if cube.ext is not None and cube.ext.maxverts >= maxverts:
        return cube.ext
    
    ext = growcubeext(cube.ext, maxverts) 
    
    if init:
        if cube.ext is not None:
            ext.surfaces = cube.ext.surfaces
            ext.verts = cube.ext.verts
        else:
            ext.surfaces = map(lambda _: SurfaceInfo(), xrange(6))
    
    cube.ext = ext
    
    return ext