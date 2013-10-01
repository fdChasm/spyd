'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.ivec import C, D, R

def dimension(orient):
    return orient>>1

def dimcoord(orient):
    return orient & 1

def opposite(orient):
    return orient ^ 1

def octadim(d):
    return 1<<d

def octacoord(d, i):
    return (i & octadim(d))>>d

def oppositeocta(d, i):
    return ((i)^octadim(D[d]))

def octaindex(d, x, y, z):
    return (((z)<<D[d])+((y)<<C[d])+((x)<<R[d]))

def octastep(x, y, z, scale):
    return ((((z)>>(scale))&1)<<2) | ((((y)>>(scale))&1)<<1) | (((x)>>(scale))&1)