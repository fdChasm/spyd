from cube2common.vec import vec

def uchar(val):
    return val&0xFF

class bvec(object):
    def __init__(self, *args):
        self.v = bytearray(3)
        
        if len(args) == 1 and isinstance(args[0], vec):
            v = args[0]
            
            self.x = uchar((v.x+1)*255/2)
            self.y = uchar((v.y+1)*255/2)
            self.z = uchar((v.z+1)*255/2)
            
        elif len(args) == 3:
            self.v = bytearray(args)
        
    def __repr__(self):
        return "<vec: {x}, {y}, {z}>".format(x=self.x, y=self.y, z=self.z)
        
    def copy(self):
        return vec(self.x, self.y, self.z)
    
    def __eq__(self, other):
        if isinstance(other, bvec):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False
        
    def __ne__(self, other):
        if isinstance(other, bvec):
            return self.x != other.x or self.y != other.y or self.z != other.z
        else:
            return False
    
    def __getitem__(self, index):
        return self.v[index]
    
    def __setitem__(self, index, value):
        self.v[index] = value
        
    @property
    def x(self):
        return self.v[0]
    
    @x.setter
    def x(self, value):
        self.v[0] = value
        
    @property
    def y(self):
        return self.v[1]
    
    @y.setter
    def y(self, value):
        self.v[1] = value
        
    @property
    def z(self):
        return self.v[2]
    
    @z.setter
    def z(self, value):
        self.v[2] = value
        
    @property
    def r(self):
        return self.v[0]
    
    @r.setter
    def r(self, value):
        self.v[0] = value
        
    @property
    def g(self):
        return self.v[1]
    
    @g.setter
    def g(self, value):
        self.v[1] = value
        
    @property
    def b(self):
        return self.v[2]
    
    @b.setter
    def b(self, value):
        self.v[2] = value
        
    def iszero(self):
        return self.x == 0 and self.y == 0 and self.z == 0
    

