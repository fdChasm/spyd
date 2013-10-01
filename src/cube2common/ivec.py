from cube2common.vec import vec

R = [1, 2, 0]
C = [2, 0, 1]
D = [0, 1, 2]

class ivec(object):
    def __init__(self, *args):
        self.v = [0]*3
        
        if len(args) == 1 and isinstance(args[0], vec):
            v = args[0]
            
            self.x = v.x
            self.y = v.y
            self.z = v.z
            
        elif len(args) == 1:
            i = args[0]
            
            self.x = ((i&1)>>0)
            self.y = ((i&2)>>1)
            self.z = ((i&4)>>2)
            
        elif len(args) == 3:
            self.v = args
            
        elif len(args) == 4:
            d, row, col, depth = args
            
            self.v[R[d]] = row;
            self.v[C[d]] = col;
            self.v[D[d]] = depth;
            
        elif len(args) == 5:
            i, cx, cy, cz, size = args
            
            self.x = cx+((i&1)>>0)*size;
            self.y = cy+((i&2)>>1)*size;
            self.z = cz+((i&4)>>2)*size;
        
    def __repr__(self):
        return "<vec: {x}, {y}, {z}>".format(x=self.x, y=self.y, z=self.z)
        
    def copy(self):
        return vec(self.x, self.y, self.z)
    
    def __eq__(self, other):
        if isinstance(other, ivec):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False
        
    def __ne__(self, other):
        if isinstance(other, ivec):
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
    
    def shl(self, n):
        self.x <<= n
        self.y <<= n
        self.z <<= n
        
    def shr(self, n):
        self.x >>= n
        self.y >>= n
        self.z >>= n
        
    def mul(self, item):
        if isinstance(item, ivec):
            self.x *= item.x
            self.y *= item.y
            self.z *= item.z
        else:
            self.x *= item
            self.y *= item
            self.z *= item
        return self
        
    def div(self, item):
        if isinstance(item, ivec):
            self.x /= item.x
            self.y /= item.y
            self.z /= item.z
        else:
            self.x /= item
            self.y /= item
            self.z /= item
        return self
        
    def add(self, item):
        if isinstance(item, ivec):
            self.x += item.x
            self.y += item.y
            self.z += item.z
        else:
            self.x += item
            self.y += item
            self.z += item
        return self
        
    def sub(self, item):
        if isinstance(item, ivec):
            self.x -= item.x
            self.y -= item.y
            self.z -= item.z
        else:
            self.x -= item
            self.y -= item
            self.z -= item
        return self
    
    def mask(self, n):
        self.x &= n
        self.y &= n
        self.z &= n
        return self
