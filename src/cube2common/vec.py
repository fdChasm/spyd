import math

class vec(object):
    v = [0]*3
    
    @staticmethod
    def from_yaw_pitch(yaw, pitch):
        x = (-math.sin(yaw)*math.cos(pitch)) 
        y = (math.cos(yaw)*math.cos(pitch))
        z = (math.sin(pitch))
        return vec(x, y, z)
    
    def __init__(self, x, y, z):
        self.v = [x, y, z]
        
    def __repr__(self):
        return "<vec: {x}, {y}, {z}>".format(x=self.x, y=self.y, z=self.z)
        
    def copy(self):
        return vec(self.x, self.y, self.z)
    
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
        
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
        
    def dist(self, vector):
        t = self.copy().sub(vector)
        return t.magnitude()
        
    def mul(self, f):
        self.x *= f
        self.y *= f
        self.z *= f
        return self
    
    def div(self, d):
        self.x /= d
        self.y /= d
        self.z /= d
        return self
    
    def iszero(self):
        return self.x == 0 and self.y == 0 and self.z == 0
    
    def rescale(self, f):
        mag = self.magnitude()
        if mag > math.exp(-6.0):
            self.mul(f / mag)
        return self
    
    def add(self, value):
        if isinstance(value, vec):
            self.x += value.x
            self.y += value.y
            self.z += value.z
        else:
            self.x += value
            self.y += value
            self.z += value
        return self
    
    def sub(self, value):
        if isinstance(value, vec):
            self.x -= value.x
            self.y -= value.y
            self.z -= value.z
        else:
            self.x -= value
            self.y -= value
            self.z -= value
        return self
    
    def dot2(self, o):
        return self.x*o.x + self.y*o.y
    
    def dot(self, o):
        return self.x*o.x + self.y*o.y + self.z*o.z
    
    def cross(self, *args):
        if len(args) == 2:
            a, b = args
            self.x = a.y*b.z-a.z*b.y; 
            self.y = a.z*b.x-a.x*b.z; 
            self.z = a.x*b.y-a.y*b.x
            return self
        elif len(args) == 3:
            o, a, b = args
            return self.cross(vec(a).sub(o), vec(b).sub(o))
