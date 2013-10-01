'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2map.facevec import facevec
def insideface(p, nump, o, numo):
    bounds = 0
    
    prev = o[numo-1]
    
    for i in xrange(numo):
    
        cur = o[i]
        d = facevec(cur.x-prev.x, cur.y-prev.y)
        
        offset = d.x*prev.y - d.y*prev.x
        
        for j in xrange(nump):
            if d.x*p[j].y - d.y*p[j].x > offset:
                return False;
           
        bounds += 1
        prev = cur
    
    return bounds >= 3
