'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
class CubeExt(object):
    va = None
    ents = [] #OctaEntities
    surfaces = [] #SufaceInfo
    verts = [] #VertInfo
    tjoins = 0
    maxverts = 0