'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.facevec import facevec
from cube2map.insideface import insideface

def clipfacevecy(o, d, cx, cy, size, r):
    if d.x >= 0:
        if cx <= o.x or cx >= o.x+d.x:
            return 0
    
    elif cx <= o.x+d.x or cx >= o.x:
        return 0

    t = (o.y-cy) + (cx-o.x)*d.y/d.x;
    if t <= 0 or t >= size:
        return 0

    r.x = cx;
    r.y = cy + t;
    return 1;

def clipfacevecx(o, d, cx, cy, size, r):
    if d.y >= 0:
        if cy <= o.y or cy >= o.y+d.y:
            return 0
    
    elif cy <= o.y+d.y or cy >= o.y:
        return 0

    t = (o.x-cx) + (cy-o.y)*d.x/d.y;
    if t <= 0 or t >= size:
        return 0

    r.x = cx + t;
    r.y = cy;
    return 1

def clipfacevec(o, d, cx, cy, size, rvecs):
    r = 0

    if o.x >= cx and o.x <= cx+size and o.y >= cy and o.y <= cy+size and ((o.x != cx and o.x != cx+size) or (o.y != cy and o.y != cy+size)):
        rvecs[0].x = o.x
        rvecs[0].y = o.y
        r += 1

    r += clipfacevecx(o, d, cx, cy, size, rvecs[r])
    r += clipfacevecx(o, d, cx, cy+size, size, rvecs[r])
    r += clipfacevecy(o, d, cx, cy, size, rvecs[r])
    r += clipfacevecy(o, d, cx+size, cy, size, rvecs[r])

    assert(r <= 2)
    return r

def clipfacevecs(o, numo, cx, cy, size, rvecs):
    cx <<= 3;
    cy <<= 3;
    size <<= 3;

    r = 0;
    prev = o[numo-1];
    for i in xrange(numo):
        cur = o[i]
        r += clipfacevec(prev, facevec(cur.x-prev.x, cur.y-prev.y), cx, cy, size, rvecs[r]);
        prev = cur
    
    corner = [facevec(cx, cy), facevec(cx+size, cy), facevec(cx+size, cy+size), facevec(cx, cy+size)];
    for i in xrange(4):
        if insideface(corner[i], 1, o, numo):
            rvecs[r] = corner[i]
            r += 1
    
    assert(r <= 8);
    return r
