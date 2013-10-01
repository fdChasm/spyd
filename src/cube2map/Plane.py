'''
This file may be in part a direct translation of the original Cube 2 sources into python.
Please see readme_source.txt for the license that may apply.
'''
from cube2common.vec import vec

class Plane(vec):
    offset = 0.0
    
    def __init__(self, *args):
        self.v = [0]*3
        if len(args) == 2:
            if isinstance(args[0], vec):
                vec.__init__(self, *(args[0].v))
            else:
                vec.__init__(self, 0.0, 0.0, 0.0)
                self.v[args[0]] = 1.0
            self.offset = args[1]
    
    def dist(self, p):
        return self.dot(p)+self.offset
    
    def __eq__(self, p):
        return self.x==p.x and self.y==p.y and self.z==p.z and self.offset==p.offset
    
    def __ne__(self, p):
        return self.x!=p.x or self.y!=p.y or self.z!=p.z or self.offset!=p.offset
    
    def toplane(self, *args):
        if len(args) == 2:
            n, p = args
            self.x = n.x
            self.y = n.y
            self.z = n.z
            self.offset = -self.dot(p)
        elif len(args) == 3:
            a, b, c = args
            self.cross(vec(b).sub(a), vec(c).sub(a))
            mag = self.magnitude()
            if mag == 0.0:
                return False
            self.div(mag)
            self.offset = -self.dot(a)
            return True