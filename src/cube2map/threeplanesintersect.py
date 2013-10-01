#@PydevCodeAnalysisIgnore
'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.vec import vec

def threeplaneintersect(pl1, pl2, pl3, dest):
    t1, t2, t3, t4 = dest, vec(), vec(), vec()
    t1.cross(pl1, pl2) 
    t4 = t1
    t1.mul(pl3.offset)
    
    t2.cross(pl3, pl1)
    t2.mul(pl2.offset)
    
    t3.cross(pl2, pl3)
    t3.mul(pl1.offset)
    
    t1.add(t2);
    t1.add(t3);
    t1.mul(-1);
    
    d = t4.dot(pl3)
    if d==0:
        return False
    
    t1.div(d)
    
    return True