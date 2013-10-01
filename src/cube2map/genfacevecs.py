'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.dimension import dimcoord
from cube2map.facevec import facevec
from cube2map.Cube import genfaceverts
from cube2common.ivec import ivec
from cube2common.constants import INT_MAX

def genfacevecs(cu, orient, pos, size, solid, fvecs, v = None):
    i = 0
    if solid:
        if orient == 0:
            if dimcoord(0):
                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1
            else:
                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1
        elif orient == 1:
            if dimcoord(1):
                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1
            else:
                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.y+size)<<3)
                    f.x = ((pos.z+size)<<3)
                    i += 1
        elif orient == 2:
            if dimcoord(2):
                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1
            else:
                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1
        elif orient == 3:
            if dimcoord(3):
                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1
            else:
                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x+size)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.x = ((pos.x)<<3)
                    f.y = ((pos.z)<<3)
                    i += 1
        elif orient == 4:
            if dimcoord(4):
                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1
            else:
                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1
        elif orient == 5:
            if dimcoord(5):
                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1
            else:
                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y+size)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x+size)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1

                    f = fvecs[i]
                    f.y = ((pos.x)<<3)
                    f.x = ((pos.y)<<3)
                    i += 1
        return 4
    buf = [ivec() for _ in xrange(4)]
    
    if v is None:
        genfaceverts(cu, orient, buf)
        v = buf
    
    prev = facevec(INT_MAX, INT_MAX)
    if orient == 0:
        if dimcoord(0):
                e = v[0]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[3]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
        else:
                e = v[3]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[0]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(0)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
    elif orient == 1:
        if dimcoord(1):
                e = v[0]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[3]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
        else:
                e = v[3]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[0]
                ef = ivec()
                ef.z = e.x
                ef.y = e.y
                ef.x = e.z
                if ef.z == dimcoord(1)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.z = pos.x
                    pf.y = pos.y
                    pf.x = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
    elif orient == 2:
        if dimcoord(2):
                e = v[0]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[3]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
        else:
                e = v[3]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[0]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(2)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
    elif orient == 3:
        if dimcoord(3):
                e = v[0]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[3]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
        else:
                e = v[3]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[0]
                ef = ivec()
                ef.x = e.x
                ef.z = e.y
                ef.y = e.z
                if ef.z == dimcoord(3)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.x = pos.x
                    pf.z = pos.y
                    pf.y = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
    elif orient == 4:
        if dimcoord(4):
                e = v[0]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[3]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
        else:
                e = v[3]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[0]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(4)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
    elif orient == 5:
        if dimcoord(5):
                e = v[0]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[3]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
        else:
                e = v[3]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[2]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[1]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1

                e = v[0]
                ef = ivec()
                ef.y = e.x
                ef.x = e.y
                ef.z = e.z
                if ef.z == dimcoord(5)*8:
                    f = fvecs[i]
                    pf = ivec()
                    pf.y = pos.x
                    pf.x = pos.y
                    pf.z = pos.z
                    f = facevec(ef.x*size + (pf.x<<3), ef.y*size + (pf.y<<3))
                    if f != prev:
                        prev = f
                        i += 1
    if fvecs[0] == prev: i -= 1
    return i
