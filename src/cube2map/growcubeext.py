'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.CubeExt import CubeExt
from cube2map.VertInfo import VertInfo

def growcubeext(old, maxverts):
    ext = CubeExt()
    ext.verts = map(lambda _: VertInfo(), xrange(maxverts))
    if old is not None:
        ext.va = old.va
        ext.ents = old.ents
        ext.tjoins = old.tjoints
    else:
        ext.va = None
        ext.ents = None
        ext.tjoints = -1
    ext.maxverts = maxverts
    return ext